<template>
  <div class="space-y-6">
    <!-- KPI 卡片区 -->
    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <!-- 今日订单 -->
      <div class="bg-white dark:bg-gray-700 rounded-lg shadow p-4 flex items-center gap-4 transition hover:shadow-md">
        <span class="text-3xl">🧾</span>
        <div class="flex-1">
          <div class="text-gray-500 dark:text-gray-300 text-sm">今日订单</div>
          <div class="text-xl font-bold">{{ kpi?.todayOrders ?? '无数据' }}</div>
        </div>
      </div>
      <!-- 今日收入 -->
      <div class="bg-white dark:bg-gray-700 rounded-lg shadow p-4 flex items-center gap-4 transition hover:shadow-md">
        <span class="text-3xl">💰</span>
        <div class="flex-1">
          <div class="text-gray-500 dark:text-gray-300 text-sm">今日收入</div>
          <div class="text-xl font-bold">{{ currency(kpi?.todayRevenue) }}</div>
        </div>
      </div>
      <!-- 新增用户 -->
      <div class="bg-white dark:bg-gray-700 rounded-lg shadow p-4 flex items-center gap-4 transition hover:shadow-md">
        <span class="text-3xl">🧑‍💼</span>
        <div class="flex-1">
          <div class="text-gray-500 dark:text-gray-300 text-sm">新增用户</div>
          <div class="text-xl font-bold">{{ kpi?.newUsers ?? '无数据' }}</div>
        </div>
      </div>
      <!-- 在线人数峰值 -->
      <div class="bg-white dark:bg-gray-700 rounded-lg shadow p-4 flex items-center gap-4 transition hover:shadow-md">
        <span class="text-3xl">📈</span>
        <div class="flex-1">
          <div class="text-gray-500 dark:text-gray-300 text-sm">在线人数峰值</div>
          <div class="text-xl font-bold">{{ kpi?.peakOnlineUsers ?? '无数据' }}</div>
        </div>
      </div>
      <!-- 5分钟内响应率 -->
      <div class="bg-white dark:bg-gray-700 rounded-lg shadow p-4 flex items-center gap-4 transition hover:shadow-md">
        <span class="text-3xl">⏱️</span>
        <div class="flex-1">
          <div class="text-gray-500 dark:text-gray-300 text-sm">5分钟内响应率</div>
          <div class="text-xl font-bold">{{ kpi?.response5min !== undefined ? kpi.response5min + '%' : '无数据' }}</div>
        </div>
      </div>
      <!-- 20分钟内出餐率 -->
      <div class="bg-white dark:bg-gray-700 rounded-lg shadow p-4 flex items-center gap-4 transition hover:shadow-md">
        <span class="text-3xl">✅</span>
        <div class="flex-1">
          <div class="text-gray-500 dark:text-gray-300 text-sm">20分钟内出餐率</div>
          <div class="text-xl font-bold">{{ kpi?.complete20min !== undefined ? kpi.complete20min + '%' : '无数据' }}</div>
        </div>
      </div>
    </div>

    <!-- 库存告警 -->
    <div v-if="inventoryAlerts && inventoryAlerts.length" class="bg-red-50 dark:bg-gray-700 border-l-4 border-red-500 p-4 rounded">
      <h3 class="font-bold text-red-700 mb-2">库存告警</h3>
      <ul>
        <li v-for="alert in inventoryAlerts" :key="alert.id" class="flex items-center justify-between">
          <span>{{ alert.text }}（数量: {{ alert.count }}）</span>
          <span>
            <span v-if="alert.confirmed" class="text-green-600">已确认</span>
            <span v-else class="text-yellow-600">未确认</span>
            <span v-if="alert.resolved" class="ml-2 text-green-600">已解决</span>
            <span v-else class="ml-2 text-red-600">未解决</span>
          </span>
        </li>
      </ul>
    </div>
    <div v-else class="bg-gray-50 dark:bg-gray-700 border-l-4 border-gray-300 p-4 rounded text-gray-500">
      无库存告警
    </div>

    <!-- 流量/销售折线图 -->
    <div class="bg-white dark:bg-gray-800 rounded shadow p-4">
      <h3 class="font-bold mb-2">流量/销售趋势</h3>
      <div v-if="trendData && trendData.length">
        <svg :width="400" :height="200">
          <polyline
            :points="lineChartPoints"
            fill="none"
            stroke="#10b981"
            stroke-width="2"
          />
          <g v-for="(item, idx) in trendData" :key="idx">
            <circle
              :cx="40 + idx * xStep"
              :cy="180 - (item.value / maxValue) * 160"
              r="3"
              fill="#10b981"
            />
          </g>
        </svg>
        <div class="flex justify-between text-xs text-gray-400 mt-2">
          <span v-for="(item, idx) in trendData" :key="idx">{{ item.label }}</span>
        </div>
      </div>
      <div v-else class="text-gray-400 text-center py-8">无数据</div>
    </div>

    <!-- 最近订单表 -->
    <div class="bg-white dark:bg-gray-800 rounded shadow p-4">
      <h3 class="font-bold mb-2">最近订单</h3>
      <table v-if="recentOrders && recentOrders.length" class="min-w-full text-sm">
        <thead>
          <tr>
            <th>订单号</th>
            <th>用户</th>
            <th>金额</th>
            <th>状态</th>
            <th>下单时间</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="order in recentOrders" :key="order.id">
            <td>{{ order.orderNo }}</td>
            <td>{{ order.username }}</td>
            <td>{{ currency(order.amount) }}</td>
            <td>{{ order.status }}</td>
            <td>{{ order.createdAt }}</td>
          </tr>
        </tbody>
      </table>
      <div v-else class="text-gray-400 text-center py-8">无数据</div>
    </div>

    <!-- 收入查询（季/月/日/历史） -->
    <div class="bg-white dark:bg-gray-800 rounded shadow p-4">
      <h3 class="font-bold mb-2">历史收入查询</h3>
      <div class="flex space-x-2 mb-2">
        <select v-model="revenueQuery.type" class="border rounded px-2 py-1">
          <option value="day">日收入</option>
          <option value="month">月收入</option>
          <option value="season">季收入</option>
        </select>
        <input v-model="revenueQuery.date" type="date" class="border rounded px-2 py-1" />
        <button class="btn" @click="fetchRevenue">查询</button>
      </div>
      <div>
        <span v-if="revenueHistory !== null">{{ currency(revenueHistory) }}</span>
        <span v-else class="text-gray-400">无数据</span>
      </div>
    </div>

    <!-- 快捷操作按钮 -->
      <div class="flex space-x-4">
<!--        <button class="btn" @click="goTo('menu')">跳转到管理后台</button>-->
        <button class="btn" @click="goTo('Audit')">系统日志</button>
        <button class="btn" @click="goTo('Reports')">订单管理</button>
        <button class="btn" @click="goTo('Settings')">报表分析</button>
<!--  &lt;!&ndash;      <button class="btn" @click="goTo('inventory')">库存管理</button>&ndash;&gt;-->
      </div>
  </div>

</template>

<script setup>
import { ref, onMounted, computed } from 'vue'

// 暂无接口对接
// import { fetchDashboardKpi, fetchInventoryAlerts, fetchRecentOrders, fetchTrendData, fetchRevenue as fetchRevenueApi } from '../api/admin'


const kpi = ref(null)
const inventoryAlerts = ref([])
const recentOrders = ref([])
const trendData = ref([])
const revenueQuery = ref({ type: 'day', date: '' })
const revenueHistory = ref(null)

// 显示默认日期为今日
const today = new Date()
const yyyy = today.getFullYear()
const mm = String(today.getMonth() + 1).padStart(2, '0')
const dd = String(today.getDate()).padStart(2, '0')
revenueQuery.value.date = `${yyyy}-${mm}-${dd}`

function goTo(section) {
  if (section === '') window.location.href = '/admin'
  else if (section === 'Audit') window.location.href = '/admin/audit'
  else if (section === 'Reports') window.location.href = '/admin/reports'
  else if (section === 'Settings') window.location.href = '/admin/settings'
  else if (section === 'orders') window.location.href = '/admin?tab=orders'
  else if (section === 'inventory') window.location.href = '/admin/inventory'
  else if (section === 'users') window.location.href = '/admin?tab=users'
  else if (section === 'menu') window.location.href = '/admin?tab=menu'
  else window.location.href = '/'
}

async function fetchAll() {
  try {
    kpi.value = await fetchDashboardKpi() || null
  } catch { kpi.value = null }
  try {
    inventoryAlerts.value = await fetchInventoryAlerts() || []
  } catch { inventoryAlerts.value = [] }
  try {
    recentOrders.value = await fetchRecentOrders() || []
  } catch { recentOrders.value = [] }
  try {
    trendData.value = await fetchTrendData() || []
  } catch { trendData.value = [] }
}

async function fetchRevenue() {
  try {
    revenueHistory.value = await fetchRevenueApi(revenueQuery.value)
  } catch {
    revenueHistory.value = null
  }
}

function currency(val) {
  if (typeof val !== 'number') return '无数据'
  return '￥' + val.toFixed(2)
}

// 折线图相关计算
const maxValue = computed(() =>
  trendData.value && trendData.value.length
    ? Math.max(...trendData.value.map(i => i.value))
    : 1
)
const xStep = computed(() =>
  trendData.value && trendData.value.length > 1
    ? 320 / (trendData.value.length - 1)
    : 0
)
const lineChartPoints = computed(() => {
  if (!trendData.value || !trendData.value.length) return ''
  return trendData.value
    .map((item, idx) => {
      const x = 40 + idx * xStep.value
      const y = 180 - (item.value / maxValue.value) * 160
      return `${x},${y}`
    })
    .join(' ')
})

onMounted(fetchAll)
</script>

<style scoped>
.btn {
  @apply px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700 transition;
}
</style>