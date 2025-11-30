<script setup>
import { ref } from 'vue'

const isDragging = ref(false)
const file = ref(null)
const uploading = ref(false)
const progress = ref(0)
const uploadStatus = ref('')

const handleDrop = (e) => {
  isDragging.value = false
  const droppedFile = e.dataTransfer.files[0]
  if (droppedFile) {
    file.value = droppedFile
  }
}

const handleFileSelect = (e) => {
  const selectedFile = e.target.files[0]
  if (selectedFile) {
    file.value = selectedFile
  }
}

const uploadFile = async () => {
  if (!file.value) return
  
  uploading.value = true
  progress.value = 0
  uploadStatus.value = '正在上传...'
  
  const formData = new FormData()
  formData.append('file', file.value)

  try {
    const response = await fetch('/api/v1/uploads/', {
      method: 'POST',
      body: formData,
    })

    if (!response.ok) {
      throw new Error('上传失败')
    }

    const data = await response.json()
    progress.value = 100
    uploadStatus.value = '上传成功！正在解析...'
    
    // Poll for status or just show success for now
    console.log('Upload success:', data)
    
    // Simulate parsing delay or redirect to data view
    setTimeout(() => {
        uploadStatus.value = `上传完成。ID: ${data.id}，状态: ${data.status}`
    }, 1000)

  } catch (error) {
    console.error('Error uploading file:', error)
    uploadStatus.value = '上传出错，请重试'
    uploading.value = false
  }
}
</script>

<template>
  <div class="max-w-3xl mx-auto">
    <h2 class="text-2xl font-bold mb-6">上传微信聊天记录</h2>
    
    <div 
      class="border-2 border-dashed rounded-lg p-12 text-center transition-colors"
      :class="isDragging ? 'border-indigo-500 bg-indigo-50' : 'border-gray-300 hover:border-indigo-400'"
      @dragover.prevent="isDragging = true"
      @dragleave.prevent="isDragging = false"
      @drop.prevent="handleDrop"
    >
      <div v-if="!file">
        <svg class="mx-auto h-12 w-12 text-gray-400" stroke="currentColor" fill="none" viewBox="0 0 48 48" aria-hidden="true">
          <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
        </svg>
        <p class="mt-1 text-sm text-gray-600">
          <button type="button" class="font-medium text-indigo-600 hover:text-indigo-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
            <label for="file-upload" class="cursor-pointer">上传文件</label>
            <input id="file-upload" name="file-upload" type="file" class="sr-only" @change="handleFileSelect">
          </button>
          或拖拽文件到此处
        </p>
        <p class="mt-1 text-xs text-gray-500">支持 TXT, CSV 格式，最大 50MB</p>

        <div class="mt-4 text-left bg-yellow-50 p-3 rounded border border-yellow-200 text-xs text-yellow-700">
          <p class="font-bold mb-1">💡 提示：微信聊天记录默认路径</p>
          <p class="font-mono bg-white px-2 py-1 rounded border border-yellow-100 select-all cursor-text">
            C:\Users\{用户名}\Documents\WeChat Files\
          </p>
          <p class="mt-1">点击上方路径可选中复制，在文件选择窗口地址栏粘贴即可快速跳转。</p>
        </div>
      </div>
      
      <div v-else class="text-left">
        <div class="flex items-center justify-between p-4 bg-gray-50 rounded">
          <span class="font-medium truncate">{{ file.name }}</span>
          <button @click="file = null" class="text-red-500 hover:text-red-700 text-sm">移除</button>
        </div>
        
        <div v-if="uploading || progress > 0" class="mt-4">
          <div class="w-full bg-gray-200 rounded-full h-2.5">
            <div class="bg-indigo-600 h-2.5 rounded-full" :style="{ width: progress + '%' }"></div>
          </div>
          <p class="text-sm text-gray-600 mt-2">{{ progress }}%</p>
        </div>
        
        <div v-if="!uploading && progress === 0" class="mt-4 text-center">
          <button @click="uploadFile" class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
            开始上传
          </button>
        </div>
        
        <div v-if="uploadStatus" class="mt-4 p-4 bg-green-50 text-green-700 rounded border border-green-200">
          {{ uploadStatus }}
        </div>
      </div>
    </div>
  </div>
</template>
