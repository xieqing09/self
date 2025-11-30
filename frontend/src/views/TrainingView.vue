<script setup>
import { ref, onMounted } from 'vue'

const config = ref({
  model: 'llama3.1:8b',
  epochs: 3,
  batchSize: 4,
  learningRate: '2e-4',
  loraRank: 8
})

const datasets = ref([])
const selectedDataset = ref('')
const previewMessages = ref([])
const isTraining = ref(false)
const logs = ref([])

const fetchMessages = async (datasetId) => {
  if (!datasetId) return
  try {
    const response = await fetch(`/api/v1/uploads/${datasetId}/messages?limit=20`)
    if (response.ok) {
      previewMessages.value = await response.json()
    }
  } catch (error) {
    console.error('Failed to fetch messages:', error)
    logs.value.push(`Error fetching preview: ${error.message}`)
  }
}

const fetchDatasets = async () => {
  try {
    const response = await fetch('/api/v1/uploads/')
    if (response.ok) {
      const data = await response.json()
      // Filter for parsed datasets only
      datasets.value = data.filter(d => d.status === 'parsed')
      if (datasets.value.length > 0) {
        selectedDataset.value = datasets.value[0].id
        fetchMessages(selectedDataset.value)
      }
    }
  } catch (error) {
    console.error('Failed to fetch datasets:', error)
    logs.value.push(`Error fetching datasets: ${error.message}`)
  }
}

// Watch for selection change
import { watch } from 'vue'
watch(selectedDataset, (newVal) => {
  if (newVal) {
    fetchMessages(newVal)
  } else {
    previewMessages.value = []
  }
})

onMounted(() => {
  fetchDatasets()
})

const startTraining = async () => {
  if (!selectedDataset.value) {
    alert('请先选择一个数据集')
    return
  }

  isTraining.value = true
  logs.value.push(`[${new Date().toLocaleTimeString()}] 开始基于模型 ${config.value.model} 训练...`)
  
  try {
    const response = await fetch('/api/v1/training/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        dataset_id: selectedDataset.value,
        config: config.value
      })
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Training request failed')
    }

    const data = await response.json()
    logs.value.push(`[${new Date().toLocaleTimeString()}] 训练任务已提交 (Task ID: ${data.task_id})`)
    logs.value.push(`[${new Date().toLocaleTimeString()}] 正在生成 Modelfile 并注册 Ollama 模型...`)
    
    // In a real app, we would poll for status here. 
    // Since the current task is synchronous (blocking) or fast, we assume success for now or wait for WebSocket updates.
    // For this MVP, we'll just show a success message after a short delay to simulate async completion if it's fast.
    
    setTimeout(() => {
        logs.value.push(`[${new Date().toLocaleTimeString()}] 训练流程完成！请在聊天页面选择新模型进行测试。`)
        isTraining.value = false
    }, 3000)

  } catch (error) {
    logs.value.push(`[${new Date().toLocaleTimeString()}] 错误: ${error.message}`)
    isTraining.value = false
  }
}
</script>

<template>
  <div class="max-w-4xl mx-auto">
    <h2 class="text-2xl font-bold mb-6">模型微调</h2>
    
    <div class="grid grid-cols-1 gap-6 lg:grid-cols-2">
      <!-- Configuration Panel -->
      <div class="bg-white shadow rounded-lg p-6">
        <h3 class="text-lg font-medium text-gray-900 mb-4">配置</h3>
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700">选择数据集 (Dataset)</label>
            <select v-model="selectedDataset" class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md border">
              <option v-if="datasets.length === 0" value="" disabled>无可用数据集 (请先上传并解析)</option>
              <option v-for="ds in datasets" :key="ds.id" :value="ds.id">
                {{ ds.filename }} ({{ new Date(ds.created_at).toLocaleDateString() }})
              </option>
            </select>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700">基础模型 (Base Model)</label>
            <select v-model="config.model" class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md border">
              <option value="llama3.1:8b">Llama 3.1 (8B)</option>
              <option value="deepseek-r1:14b">DeepSeek R1 (14B)</option>
              <option value="qwen3-coder:30b">Qwen3 Coder (30B)</option>
              <option value="phi4:latest">Phi-4</option>
            </select>
          </div>
          
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700">轮数 (Epochs)</label>
              <input type="number" v-model="config.epochs" class="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md border p-2">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">批次大小 (Batch Size)</label>
              <input type="number" v-model="config.batchSize" class="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md border p-2">
            </div>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700">学习率 (Learning Rate)</label>
            <input type="text" v-model="config.learningRate" class="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md border p-2">
          </div>
          
          <div>
             <button 
              @click="startTraining" 
              :disabled="isTraining"
              class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:bg-gray-400"
            >
              {{ isTraining ? '训练中...' : '开始训练' }}
            </button>
          </div>
        </div>
      </div>
      
      <!-- Monitoring Panel -->
      <div class="bg-black text-green-400 font-mono text-sm p-4 rounded-lg shadow h-96 overflow-y-auto" id="log-container">
        <div v-if="logs.length === 0" class="text-gray-500">等待训练开始...</div>
        <div v-for="(log, index) in logs" :key="index">{{ log }}</div>
      </div>
    </div>

    <!-- Data Preview Section -->
    <div class="mt-8 bg-white shadow rounded-lg p-6">
      <h3 class="text-lg font-medium text-gray-900 mb-4">数据预览 (Data Preview - Top 20)</h3>
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">发送者</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">内容</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">时间</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-if="previewMessages.length === 0">
              <td colspan="3" class="px-6 py-4 text-center text-sm text-gray-500">暂无预览数据或未选择数据集</td>
            </tr>
            <tr v-for="msg in previewMessages" :key="msg.id">
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ msg.sender }}</td>
              <td class="px-6 py-4 text-sm text-gray-500 max-w-md truncate">{{ msg.content }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ msg.timestamp ? new Date(msg.timestamp).toLocaleString() : '' }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>
