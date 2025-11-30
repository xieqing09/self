<template>
  <div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
    <div class="px-4 py-6 sm:px-0">
      <h1 class="text-3xl font-bold text-gray-900 mb-6">欢迎使用微信聊天记录微调平台</h1>
      <div class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
        <div class="bg-white overflow-hidden shadow rounded-lg p-6">
          <h3 class="text-lg font-medium text-gray-900">上传数据</h3>
          <p class="mt-2 text-sm text-gray-500">上传您的微信聊天记录进行处理。</p>
          <div class="mt-4">
            <router-link to="/upload" class="text-indigo-600 hover:text-indigo-900">前往上传 &rarr;</router-link>
          </div>
        </div>
        <div class="bg-white overflow-hidden shadow rounded-lg p-6">
          <h3 class="text-lg font-medium text-gray-900">数据标注</h3>
          <p class="mt-2 text-sm text-gray-500">查看并标注处理后的聊天数据。</p>
          <div class="mt-4">
            <router-link to="/data" class="text-indigo-600 hover:text-indigo-900">前往数据 &rarr;</router-link>
          </div>
        </div>
        <div class="bg-white overflow-hidden shadow rounded-lg p-6">
          <h3 class="text-lg font-medium text-gray-900">模型训练</h3>
          <p class="mt-2 text-sm text-gray-500">使用标注数据对模型进行微调。</p>
          <div class="mt-4">
            <router-link to="/training" class="text-indigo-600 hover:text-indigo-900">前往训练 &rarr;</router-link>
          </div>
        </div>
        <div class="bg-white overflow-hidden shadow rounded-lg p-6">
          <h3 class="text-lg font-medium text-gray-900">在线对话</h3>
          <p class="mt-2 text-sm text-gray-500">在对话界面测试微调后的模型。</p>
          <div class="mt-4">
            <router-link to="/chat" class="text-indigo-600 hover:text-indigo-900">前往对话 &rarr;</router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
