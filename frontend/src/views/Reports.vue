<template>
  <div class="p-6">
    <h2 class="text-xl font-bold mb-4">报表/分析</h2>
    <div class="flex flex-wrap gap-4 mb-4">
      <select v-model="slice" class="border rounded px-2 py-1">
        <option value="day">按日</option>
        <option value="week">按周</option>
        <option value="month">按月</option>
      </select>
      <select v-model="type" class="border rounded px-2 py-1">
        <option value="sales">销售额</option>
        <option value="items">菜品排名</option>
      </select>
      <button class="bg-green-600 text-white px-4 py-1 rounded" @click="fetchReport">查询</button>
      <button class="bg-blue-600 text-white px-4 py-1 rounded" @click="exportCSV">导出CSV</button>
      <button class="bg-gray-600 text-white px-4 py-1 rounded" @click="exportPDF">导出PDF</button>
      <button class="bg-yellow-600 text-white px-4 py-1 rounded" @click="toggleView">{{ view === 'chart' ? '表格' : '图表' }}</button>
    </div>
    <div v-if="view === 'chart'" class="mb-4">
      <!-- 简单柱状图 -->
      <svg width="400" height="200">
        <g v-for="(item, idx) in reportData" :key="idx">
          <rect
            :x="40 + idx * 60"
            :y="180 - (item.value / maxValue) * 160"
            width="40"
            :height="(item.value / maxValue) * 160"
            fill="#10b981"
          />
          <text :x="60 + idx * 60" y="195" text-anchor="middle" font-size="12">{{ item.label }}</text>
          <text :x="60 + idx * 60" :y="170 - (item.value / maxValue) * 160" text-anchor="middle" font-size="12">{{ item.value }}</text>
        </g>
      </svg>
    </div>
    <div v-else>
      <table class="min-w-full text-sm border">
        <thead>
          <tr>
            <th class="border px-2 py-1">维度</th>
            <th class="border px-2 py-1">数值</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in reportData" :key="item.label">
            <td class="border px-2 py-1">{{ item.label }}</td>
            <td class="border px-2 py-1">{{ item.value }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-if="reportData.length === 0" class="text-gray-400 mt-4">暂无数据</div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const slice = ref('day')
const type = ref('sales')
const view = ref('chart')
const reportData = ref([])

function fetchReport() {
  // 伪数据，实际应通过GET /admin/reports?slice=...&type=...获取
  if (type.value === 'sales') {
    reportData.value = [
      { label: '2026-05-18', value: 1200 },
      { label: '2026-05-19', value: 1500 },
      { label: '2026-05-20', value: 900 }
    ]
  } else {
    reportData.value = [
      { label: '可乐', value: 320 },
      { label: '薯条', value: 210 },
      { label: '汉堡', value: 180 }
    ]
  }
}
const maxValue = computed(() =>
  reportData.value.length ? Math.max(...reportData.value.map(i => i.value)) : 1
)
function exportCSV() {
  const csv = ['维度,数值']
  reportData.value.forEach(item => {
    csv.push([item.label, item.value].join(','))
  })
  const blob = new Blob([csv.join('\n')], { type: 'text/csv' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = 'report.csv'
  a.click()
  URL.revokeObjectURL(url)
}
function exportPDF() {
  alert('PDF导出功能请用专业库实现，此处为占位')
}
function toggleView() {
  view.value = view.value === 'chart' ? 'table' : 'chart'
}
fetchReport()
</script>
