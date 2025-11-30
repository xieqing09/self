# 微信聊天记录上传与模型微调系统 —— 后端开发文档

> 本文档详细描述网站后端的架构设计、模块说明、技术细节、数据流程、API 设计、任务队列、模型训练与部署、数据库设计、安全策略等内容。可作为完整后端实现的技术蓝图。

---

## 目录
1. 后端总体概述
2. 技术架构与技术栈
3. 系统模块分层设计
4. 数据库设计（MySQL）
5. 对象存储（MinIO / S3 兼容）
6. API 设计（FastAPI）
7. 异步任务队列（Celery + Redis）
8. 微信聊天记录解析模块
9. 自动打标模块
10. 训练数据导出模块
11. 模型微调模块（LoRA / PEFT）
12. 模型推理服务集成
13. 安全策略与访问控制
14. 日志、监控与错误处理
15. 部署说明（Docker + Docker Compose）
16. 后端目录结构规范
17. 后续扩展说明

---

## 1. 后端总体概述
后端负责完成从聊天记录上传、解析、打标、训练、推理等完整流程，核心功能包括：
- 文件上传与对象存储管理
- 聊天记录解析（txt / html / csv / 其他微信格式）
- 自动语义打标（规则 + 模型）
- 数据集版本管理与训练集导出
- 调度微调任务（LoRA）
- 管理与调用训练后的模型
- 提供对话推理 API
- 记录用户数据、任务状态、训练版本

后端基于 **FastAPI + Celery + MySQL + Redis + MinIO** 组合构建，满足高扩展性与任务异步化需求。

---

## 2. 技术架构与技术栈
### 核心技术
- **FastAPI**：REST API 框架，支持异步，高性能
- **Celery + Redis**：解析、打标、训练的异步任务队列
- **MySQL + SQLAlchemy**：结构化数据存储
- **MinIO（S3 兼容）**：存储上传聊天记录与导出数据
- **aiomysql**：异步 MySQL 驱动
- **Pydantic**：数据验证与序列化
- **Docker Compose**：开发环境一键部署

---

## 3. 系统模块分层设计
```
backend/
 ├── app/
 │   ├── api/                # 请求处理
 │   ├── workers/            # Celery Worker
 │   ├── utils/              # 工具模块
 │   ├── models.py           # ORM 模型
 │   ├── schemas.py          # Pydantic 模型
 │   ├── crud.py             # 数据访问层
 │   ├── db.py               # MySQL 连接管理
 │   ├── tasks.py            # Celery 主入口
 │   └── main.py             # FastAPI 入口
 ├── docker-compose.yml
 ├── Dockerfile
 ├── .env
 └── requirements.txt
```

---

## 4. 数据库设计（MySQL）
考虑 MySQL 的兼容性：
- **UUID 使用 CHAR(32)**
- **JSON 字段使用 MySQL 原生 JSON**

### 主要数据表
#### 4.1 `users`
存储用户信息
- id (CHAR32)
- email
- name

#### 4.2 `uploads`
存储上传文件的信息
- id
- user_id
- filename
- storage_path
- status（uploaded / parsing / parsed / failed）

#### 4.3 `messages`
解析后的聊天记录
- id
- upload_id
- sender
- text
- timestamp
- raw（JSON）

#### 4.4 `labels`
自动/人工标注信息
- message_id
- label（JSON）
- source（rule / model / human）

---

## 5. 对象存储（MinIO）
后端使用 MinIO 来存储文件：
- 上传聊天记录（txt / html / zip）
- 导出的训练集（jsonl）
- 模型训练的产物（checkpoint）

提供统一的工具模块：
- `upload_fileobj(file_obj, bucket, key)`

---

## 6. API 设计（FastAPI）
### 6.1 上传聊天记录
```
POST /api/v1/uploads
```
表单上传文件，写入 MinIO，并生成 upload 记录。

### 6.2 获取解析状态
```
GET /api/v1/uploads/{upload_id}/status
```

### 6.3 获取解析后的消息
```
GET /api/v1/messages?upload_id=xxx
```

### 6.4 启动训练任务
```
POST /api/v1/train/start
```

### 6.5 模型推理
```
POST /api/v1/model/chat
```

---

## 7. 异步任务队列（Celery + Redis）
Celery 用于处理 CPU/IO 密集任务，例如：
- 文件解析
- 自动打标
- 导出训练数据
- 模型训练

### 队列任务：
- `parse_upload`
- `auto_label_messages`
- `train_model`

使用多 worker 隔离：
- parser-worker
- label-worker
- trainer-worker

---

## 8. 微信聊天记录解析模块
解析支持格式：
- txt（最常见）
- html（PC 微信导出）
- csv（部分手机导出工具生成）

解析流程：
1. 下载 MinIO 中的文件
2. 自动识别文件类型
3. 按正则匹配行模式拆分消息
4. 生成 message 对象写入 MySQL

---

## 9. 自动打标模块
打标采用 **规则 + 小模型** 混合方式：

### 规则示例：
- 包含“工资”、“欠薪” → topic = 工资纠纷
- 包含“谢谢”、表情符号 → sentiment = positive

### 模型打标（可选）：
使用 BERT 分类模型：
- 情绪分类（积极 / 中性 / 消极）
- 意图分类（咨询 / 请求 / 抱怨）
- 话题分类（多个）

---

## 10. 训练数据导出
以 JSONL 格式导出适用于 LoRA 微调的数据：
```
{"prompt": "用户: ...", "completion": "回复: ..."}
```

数据版本会写入 MinIO。

---

## 11. 模型微调模块
支持：
- 全量微调（资源需求大）
- **LoRA 微调**（推荐）

训练流程由 Celery 触发：
1. 下载数据集
2. 载入基础模型（如 Qwen、Llama2）
3. LoRA 参数配置
4. 训练与评估
5. 将模型权重上传到 MinIO
6. 返回 model_id

---

## 12. 模型推理服务
后端支持两种方式：
1. 本地加载微调模型（适合小模型）
2. 独立 GPU 推理服务（推荐部署在单独容器中）

前端通过 API 调用：
```
POST /api/v1/model/chat
```
支持流式 SSE 或一次性输出。

---

## 13. 安全策略与访问控制
- 用户上传文件必须授权
- 文件扫描与大小限制
- API 使用 JWT / Token 验证
- MySQL 权限最小化
- 模型推理结果敏感信息过滤

---

## 14. 日志、监控与错误处理
- 访问日志：FastAPI 内置
- 任务日志：Celery Worker 输出
- 数据日志：MySQL 版本记录
- 监控：Prometheus + Grafana（可选）

---

## 15. 部署说明
使用 `docker-compose` 可以一键拉起服务：
```
docker-compose up --build
```
服务包含：
- backend（FastAPI）
- worker（Celery）
- MySQL
- Redis
- MinIO

---

## 16. 后端目录结构规范
见文档顶部目录结构，建议保持此结构，方便扩展。

---

## 17. 后续扩展方向
- 群聊高维结构分析
- 用户角色识别（A/B/C 多方）
- 事件抽取（例如：欠薪纠纷事件）
- 训练自动化（AutoTrain）
- 多模型版本组织（模型仓库）
- 接入前端标注工具

---

如需，我还可以：
- 生成 **后端 API 文档（OpenAPI 规范）**
- 生成 **后端真实代码骨架（包含完整文件）**
- 生成 **MySQL 数据库 ER 图**
- 生成 **部署指南 PDF / Markdown**


