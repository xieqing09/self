
```

## 5. 数据流与处理管线
*(待补充)*

## 6. 微信聊天记录采集与解析
*(待补充)*

## 7. 自动打标（标注）策略
*(待补充)*

## 8. 数据存储与版本控制
*(待补充)*

## 9. 模型微调（训练）方案
*(待补充)*

## 10. 模型部署与在线推理
*(待补充)*

## 11. 前端实现细节

### 11.1 项目初始化
- **脚手架**: Vite
- **框架**: Vue 3 (Composition API)
- **语言**: TypeScript (推荐) 或 JavaScript
- **样式**: Tailwind CSS
- **状态管理**: Pinia
- **路由**: Vue Router

### 11.2 目录结构
```
src/
├── assets/          # 静态资源
├── components/      # 公共组件 (Button, Modal, ChatBubble, etc.)
├── layouts/         # 布局组件 (Sidebar, Header)
├── stores/          # Pinia 状态管理
├── views/           # 页面视图
│   ├── HomeView.vue        # 仪表盘
│   ├── UploadView.vue      # 上传与解析状态
│   ├── DataView.vue        # 数据预览与标注
│   ├── TrainingView.vue    # 模型训练配置与监控
│   └── ChatView.vue        # 在线对话测试
├── router/          # 路由配置
├── services/        # API 请求封装 (Axios)
└── utils/           # 工具函数 (格式化时间, 文件处理)
```

### 11.3 核心功能模块

#### 11.3.1 上传模块 (UploadView)
- **功能**: 支持拖拽上传 `.txt`, `.csv` 或微信导出格式文件。
- **交互**: 
  - 显示上传进度条。
  - 上传完成后自动轮询解析任务状态。
  - 解析完成后显示简报（消息条数、用户数）。

#### 11.3.2 数据清洗与标注 (DataView)
- **功能**: 展示解析后的聊天记录列表。
- **交互**: 
  - 提供搜索和过滤功能。
  - 支持手动修正错误的标注（如角色分类错误）。
  - "确认数据集" 按钮，将数据锁定版本用于训练。

#### 11.3.3 模型微调配置 (TrainingView)
- **功能**: 配置训练参数。
- **参数**:
  - Base Model (e.g., Qwen, ChatGLM)
  - Epochs, Batch Size, Learning Rate
  - LoRA Rank/Alpha
- **可视化**: 实时展示 Loss 曲线 (使用 ECharts 或 Chart.js)。

#### 11.3.4 在线对话 (ChatView)
- **功能**: 与微调后的模型进行交互。
- **UI**: 仿微信聊天界面。
- **特性**: 
  - 支持流式输出 (Streaming Response).
  - 显示推理耗时。
  - 支持多轮对话。

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
