<template>
  <div class="p-6">
    <h2 class="text-xl font-bold mb-4">审计日志与操作历史</h2>
    <div class="flex flex-wrap gap-4 mb-4">
      <input v-model="filter.user" placeholder="用户" class="border rounded px-2 py-1" />
      <input v-model="filter.action" placeholder="操作" class="border rounded px-2 py-1" />
      <input v-model="filter.time" type="date" class="border rounded px-2 py-1" />
      <button class="bg-green-600 text-white px-4 py-1 rounded" @click="fetchLogs">筛选</button>
      <button class="bg-blue-600 text-white px-4 py-1 rounded" @click="exportLogs">导出</button>
    </div>
    <div class="border-l-4 border-green-500 pl-4">
      <div v-for="log in filteredLogs" :key="log.id" class="mb-4">
        <div class="text-gray-500 text-xs">{{ log.time }} - {{ log.user }}</div>
        <div class="font-semibold">{{ log.action }}</div>
        <div class="text-gray-400 text-sm">{{ log.detail }}</div>
      </div>
      <div v-if="filteredLogs.length === 0" class="text-gray-400">暂无日志</div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const logs = ref([])
const filter = ref({ user: '', action: '', time: '' })

function fetchLogs() {
  // 演示用数据
  logs.value = [
    { id: 1, user: 'admin', action: '修改菜单', detail: '将“甜甜花酿鸡”价格改为5元', time: '2026-05-20 10:01' },
    { id: 2, user: 'admin', action: '订单改动', detail: '订单#12345状态改为已完成', time: '2026-05-20 09:50' },
    { id: 3, user: 'alice', action: '修改菜单', detail: '下架“奇巧零食”', time: '2026-05-19 18:22' }
  ]
}

const filteredLogs = computed(() => {
  return logs.value.filter(log =>
    (!filter.value.user || log.user.includes(filter.value.user)) &&
    (!filter.value.action || log.action.includes(filter.value.action)) &&
    (!filter.value.time || log.time.startsWith(filter.value.time))
  )
})

function exportLogs() {
  const csv = ['用户,操作,详情,时间']
  filteredLogs.value.forEach(log => {
    csv.push([log.user, log.action, log.detail, log.time].join(','))
  })
  const blob = new Blob([csv.join('\n')], { type: 'text/csv' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = 'audit_logs.csv'
  a.click()
  URL.revokeObjectURL(url)
}

onMounted(fetchLogs)
</script>