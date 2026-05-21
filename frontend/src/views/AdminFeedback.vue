<template>
  <div>
    <div class="flex items-center justify-between mb-3">
      <h2 class="text-lg font-bold text-gray-900 dark:text-gray-100">反馈管理</h2>
    </div>
    <table class="w-full text-sm border border-gray-300 dark:border-gray-700">
      <thead class="bg-gray-100 dark:bg-gray-700">
        <tr class="text-gray-900 dark:text-gray-100">
          <th class="border border-gray-300 dark:border-gray-700 px-2 py-1">ID</th>
          <th class="border border-gray-300 dark:border-gray-700 px-2 py-1">用户</th>
          <th class="border border-gray-300 dark:border-gray-700 px-2 py-1">反馈内容</th>
          <th class="border border-gray-300 dark:border-gray-700 px-2 py-1">提交时间</th>
          <th class="border border-gray-300 dark:border-gray-700 px-2 py-1">操作</th>
        </tr>
      </thead>
      <tbody class="text-gray-800 dark:text-gray-200">
        <tr
          v-for="feedback in feedbacks"
          :key="feedback.id"
          class="hover:bg-gray-50 dark:hover:bg-gray-700"
        >
          <td class="border border-gray-300 dark:border-gray-700 px-2 py-1">{{ feedback.id }}</td>
          <td class="border border-gray-300 dark:border-gray-700 px-2 py-1">{{ feedback.username || '匿名用户' }}</td>
          <td class="border border-gray-300 dark:border-gray-700 px-2 py-1 max-w-xs truncate">
            {{ feedback.content }}
          </td>
          <td class="border border-gray-300 dark:border-gray-700 px-2 py-1">
            {{ formatTime(feedback.created_at) }}
          </td>
          <td class="border border-gray-300 dark:border-gray-700 px-2 py-1">
            <button
              class="px-2 py-1 text-xs bg-red-500 text-white rounded hover:bg-red-600 dark:hover:bg-red-400"
              @click="remove(feedback.id)"
            >
              删除
            </button>
          </td>
        </tr>
      </tbody>
    </table>

    <p v-if="error" class="text-red-500 text-xs mt-2">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'

const props = defineProps({
  token: { type: String, required: true }
})

const feedbacks = ref([])
const error = ref('')

const formatTime = (timeStr) => {
  if (!timeStr) return '-'
  const date = new Date(timeStr)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const fetchFeedbacks = async () => {
  error.value = ''
  const res = await fetch('http://127.0.0.1:8000/admin/feedback/', {
    headers: {
      Authorization: `Bearer ${props.token}`
    }
  })
  if (res.ok) {
    feedbacks.value = await res.json()
  } else {
    error.value = '获取反馈失败'
  }
}

const remove = async (id) => {
  if (!confirm('确认删除该反馈？')) return
  const res = await fetch(`http://127.0.0.1:8000/admin/feedback/${id}`, {
    method: 'DELETE',
    headers: {
      Authorization: `Bearer ${props.token}`
    }
  })
  if (res.ok) {
    await fetchFeedbacks()
  } else {
    error.value = '删除失败'
  }
}

onMounted(fetchFeedbacks)
watch(() => props.token, () => {
  if (props.token) fetchFeedbacks()
})
</script>