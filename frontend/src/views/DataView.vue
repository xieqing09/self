<script setup>
import { ref } from 'vue'

const messages = ref([
  { id: 1, sender: '用户 A', content: '你好，最近怎么样？', role: 'user', timestamp: '2023-10-01 10:00:00' },
  { id: 2, sender: '用户 B', content: '我很好，谢谢。你呢？', role: 'assistant', timestamp: '2023-10-01 10:00:05' },
  { id: 3, sender: '用户 A', content: '挺好的。你能帮我看看这个 Python 问题吗？', role: 'user', timestamp: '2023-10-01 10:01:00' },
  { id: 4, sender: '用户 B', content: '当然，你需要什么帮助？', role: 'assistant', timestamp: '2023-10-01 10:01:30' },
])

const toggleRole = (msg) => {
  msg.role = msg.role === 'user' ? 'assistant' : 'user'
}
</script>

<template>
  <div class="max-w-5xl mx-auto">
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-2xl font-bold">数据预览与标注</h2>
      <button class="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700">确认数据集</button>
    </div>

    <div class="bg-white shadow overflow-hidden border-b border-gray-200 sm:rounded-lg">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">时间</th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">发送者</th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">内容</th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">角色 (点击切换)</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="msg in messages" :key="msg.id">
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ msg.timestamp }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ msg.sender }}</td>
            <td class="px-6 py-4 text-sm text-gray-500">{{ msg.content }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm">
              <span 
                @click="toggleRole(msg)"
                class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full cursor-pointer select-none"
                :class="msg.role === 'user' ? 'bg-blue-100 text-blue-800' : 'bg-green-100 text-green-800'"
              >
                {{ msg.role }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
