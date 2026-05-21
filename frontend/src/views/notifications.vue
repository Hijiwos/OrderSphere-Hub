<template>
  <div class="max-w-3xl mx-auto mt-10 bg-white dark:bg-gray-800 p-6 rounded shadow">
    <h2 class="text-2xl font-bold mb-4 text-center">通知中心</h2>

    <!-- 工具栏 -->
    <div class="flex flex-wrap gap-2 justify-between mb-4">
      <div class="flex gap-2">
        <button
          @click="filterType = 'all'"
          :class="filterType === 'all' ? 'btn-primary' : 'btn-outline'"
        >
          全部
        </button>
        <button
          @click="filterType = 'unread'"
          :class="filterType === 'unread' ? 'btn-primary' : 'btn-outline'"
        >
          未读
          <span v-if="unreadCount > 0" class="bg-red-500 text-white text-xs px-1.5 rounded-full ml-1">
            {{ unreadCount }}
          </span>
        </button>
      </div>
      <div class="flex gap-2">
        <button
          @click="markAllAsRead"
          class="btn-outline text-sm"
        >
          全部已读
        </button>
        <button
          @click="clearAll"
          class="btn-outline text-red-600"
        >
          清空通知
        </button>
      </div>
    </div>

    <!-- 通知列表 -->
    <div class="space-y-3 max-h-[600px] overflow-y-auto pr-1">
      <div
        v-for="item in filteredList"
        :key="item.id"
        class="p-3 rounded border dark:border-gray-700 transition"
        :class="item.is_read ? 'bg-gray-50 dark:bg-gray-700/50' : 'bg-blue-50 dark:bg-blue-900/20 border-blue-200'"
        @click="markAsRead(item)"
      >
        <div class="flex justify-between items-start">
          <div class="font-medium text-gray-900 dark:text-gray-100">
            {{ item.title }}
            <span v-if="!item.is_read" class="ml-2 inline-block w-2 h-2 bg-red-500 rounded-full"></span>
          </div>
          <span class="text-xs text-gray-500 whitespace-nowrap ml-2">
            {{ item.created_at }}
          </span>
        </div>
        <p class="text-sm text-gray-600 dark:text-gray-300 mt-1">
          {{ item.content }}
        </p>
      </div>

      <div v-if="filteredList.length === 0" class="text-center text-gray-500 py-10">
        暂无通知
      </div>
    </div>

    <!-- 状态提示 -->
    <p v-if="success" class="text-green-600 text-sm mt-4 text-center">{{ success }}</p>
    <p v-if="error" class="text-red-500 text-sm mt-4 text-center">{{ error }}</p>
  </div>
</template>

<script setup>
import { reactive, ref, computed, onMounted, onUnmounted } from 'vue'

const token = localStorage.getItem('token')
const api = 'http://127.0.0.1:8000/notifications'

// 通知列表
const list = ref([])
const filterType = ref('all') // all / unread

// 提示
const error = ref('')
const success = ref('')

// WebSocket 连接（实时推送）
let ws = null

// 获取通知列表
async function getList() {
  try {
    const res = await fetch(api, {
      headers: { Authorization: `Bearer ${token}` }
    })
    if (!res.ok) return
    list.value = await res.json()
  } catch (e) {
    error.value = '获取通知失败'
  }
}

// 筛选：全部 / 未读
const filteredList = computed(() => {
  if (filterType.value === 'unread') {
    return list.value.filter(item => !item.is_read)
  }
  return list.value
})

// 未读数量
const unreadCount = computed(() => {
  return list.value.filter(item => !item.is_read).length
})

// 标记单条已读
async function markAsRead(item) {
  if (item.is_read) return
  try {
    await fetch(`${api}/${item.id}/read`, {
      method: 'PUT',
      headers: { Authorization: `Bearer ${token}` }
    })
    item.is_read = true
    success.value = '已标记为已读'
    setTimeout(() => success.value = '', 1500)
  } catch (e) {}
}

// 全部已读
async function markAllAsRead() {
  try {
    await fetch(`${api}/read-all`, {
      method: 'PUT',
      headers: { Authorization: `Bearer ${token}` }
    })
    list.value.forEach(item => item.is_read = true)
    success.value = '全部标记为已读'
    setTimeout(() => success.value = '', 1500)
  } catch (e) {
    error.value = '操作失败'
  }
}

// 清空通知
async function clearAll() {
  if (!confirm('确定清空所有通知？')) return
  try {
    await fetch(api, {
      method: 'DELETE',
      headers: { Authorization: `Bearer ${token}` }
    })
    list.value = []
    success.value = '已清空所有通知'
    setTimeout(() => success.value = '', 1500)
  } catch (e) {
    error.value = '清空失败'
  }
}

// WebSocket 实时接收新通知
function connectWebSocket() {
  const wsUrl = `ws://127.0.0.1:8000/ws?token=${token}`
  ws = new WebSocket(wsUrl)

  ws.onmessage = (e) => {
    const data = JSON.parse(e.data)
    if (data.type === 'notification') {
      list.value.unshift(data.data)
    }
  }

  ws.onclose = () => {
    setTimeout(connectWebSocket, 3000)
  }
}

// 生命周期
onMounted(() => {
  getList()
  connectWebSocket()
})

onUnmounted(() => {
  if (ws) ws.close()
})
</script>

<style scoped>
.input {
  @apply w-full border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 p-2 rounded mb-3;
}
.btn-primary {
  @apply bg-blue-600 text-white py-1.5 px-3 rounded hover:bg-blue-700 transition text-sm;
}
.btn-outline {
  @apply border border-gray-300 dark:border-gray-600 py-1.5 px-3 rounded hover:bg-gray-100 dark:hover:bg-gray-700 transition text-sm;
}
</style>