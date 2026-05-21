<template>
  <div class="min-h-screen bg-gray-100 dark:bg-gray-900 py-8">
    <div class="max-w-2xl mx-auto bg-white dark:bg-gray-800 rounded-lg shadow p-6">
      <h2 class="text-2xl font-bold text-center text-gray-900 dark:text-white mb-6">问题反馈</h2>
      <p class="text-sm text-gray-500 dark:text-gray-400 mb-4">
        填写使用中遇到的问题或优化建议，我们会及时查看处理
      </p>

      <textarea
        v-model="content"
        class="w-full h-40 border border-gray-300 dark:border-gray-700 rounded p-3 resize-none bg-white dark:bg-gray-900 dark:text-gray-100"
        placeholder="请输入你的反馈内容..."
      ></textarea>

      <div class="mt-5 text-center">
        <button
          @click="submitFeed"
          class="px-10 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition"
        >
          提交反馈
        </button>
      </div>

      <p v-if="msg" class="text-center mt-3 text-sm" :class="isOk?'text-green-500':'text-red-500'">
        {{ msg }}
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const content = ref('')
const msg = ref('')
const isOk = ref(false)
const token = ref(localStorage.getItem('token') || '')

const submitFeed = async () => {
  if (!token.value) {
    msg.value = '请先登录！'
    isOk.value = false
    return
  }
  if (!content.value.trim()) {
    msg.value = '反馈内容不能为空'
    isOk.value = false
    return
  }

  try {
    const res = await fetch('http://127.0.0.1:8000/feedback/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token.value}`
      },
      body: JSON.stringify({ content: content.value })
    })
    if (res.ok) {
      msg.value = '反馈提交成功！'
      isOk.value = true
      content.value = ''
    } else {
      msg.value = '提交失败'
      isOk.value = false
    }
  } catch (err) {
    msg.value = '网络错误'
    isOk.value = false
  }
}
</script>