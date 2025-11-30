<script setup>
import { ref, onMounted } from 'vue'

const selectedModel = ref('llama3.1:8b')
const availableModels = ref([])
const input = ref('')
const messages = ref([
  { role: 'assistant', content: '您好！我是您的微调助手，今天有什么可以帮您？' }
])
const isLoading = ref(false)

const fetchModels = async () => {
  try {
    const response = await fetch('/api/v1/models/')
    if (response.ok) {
      const data = await response.json()
      if (data.models && Array.isArray(data.models)) {
        availableModels.value = data.models.map(m => ({
          name: m.name,
          value: m.name
        }))
        
        // If current selected model is not in the list, select the first one
        const exists = availableModels.value.find(m => m.value === selectedModel.value)
        if (!exists && availableModels.value.length > 0) {
          // Prefer llama3.1:8b if available, otherwise first
          const llama = availableModels.value.find(m => m.value.includes('llama3.1'))
          selectedModel.value = llama ? llama.value : availableModels.value[0].value
        }
      }
    }
  } catch (error) {
    console.error('Failed to fetch models:', error)
    // Fallback
    availableModels.value = [
      { name: 'Llama 3.1 (8B)', value: 'llama3.1:8b' },
      { name: 'DeepSeek R1 (14B)', value: 'deepseek-r1:14b' }
    ]
  }
}

onMounted(() => {
  fetchModels()
})

const sendMessage = async () => {
  if (!input.value.trim()) return
  
  const userMsg = input.value
  messages.value.push({ role: 'user', content: userMsg })
  input.value = ''
  isLoading.value = true
  
  try {
    // Prepare history (exclude the just added user message)
    const history = messages.value.slice(0, -1).map(m => ({
      role: m.role,
      content: m.content
    }))

    const response = await fetch('/api/v1/chat/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message: userMsg,
        model: selectedModel.value,
        history: history
      })
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      throw new Error(errorData.detail || 'API request failed')
    }

    const data = await response.json()
    messages.value.push({ role: 'assistant', content: data.response })
  } catch (error) {
    console.error('Chat error:', error)
    messages.value.push({ role: 'assistant', content: `Error: ${error.message}` })
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="max-w-2xl mx-auto h-[600px] flex flex-col bg-white shadow rounded-lg overflow-hidden">
    <div class="bg-gray-100 p-4 border-b flex justify-between items-center">
      <h3 class="font-medium text-gray-700">与模型对话</h3>
      <select v-model="selectedModel" class="text-sm border-gray-300 rounded-md shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50">
        <option v-for="model in availableModels" :key="model.value" :value="model.value">
          {{ model.name }}
        </option>
      </select>
    </div>
    
    <div class="flex-1 overflow-y-auto p-4 space-y-4">
      <div 
        v-for="(msg, idx) in messages" 
        :key="idx" 
        class="flex"
        :class="msg.role === 'user' ? 'justify-end' : 'justify-start'"
      >
        <div 
          class="max-w-[80%] rounded-lg px-4 py-2"
          :class="msg.role === 'user' ? 'bg-indigo-600 text-white' : 'bg-gray-200 text-gray-900'"
        >
          {{ msg.content }}
        </div>
      </div>
      <div v-if="isLoading" class="flex justify-start">
        <div class="bg-gray-200 text-gray-500 rounded-lg px-4 py-2">
          思考中...
        </div>
      </div>
    </div>
    
    <div class="p-4 border-t bg-gray-50">
      <div class="flex space-x-2">
        <input 
          v-model="input" 
          @keyup.enter="sendMessage"
          type="text" 
          class="flex-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full rounded-md border-gray-300 border p-2" 
          placeholder="输入您的消息..."
        >
        <button 
          @click="sendMessage"
          class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
        >
          发送
        </button>
      </div>
    </div>
  </div>
</template>
