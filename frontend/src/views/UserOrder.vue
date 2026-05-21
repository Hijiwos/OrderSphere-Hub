<template>
  <div class="min-h-screen bg-gray-100 dark:bg-gray-900 py-6">
    <div class="max-w-4xl mx-auto bg-white dark:bg-gray-800 rounded shadow p-6">
      <h2 class="text-xl font-bold text-gray-900 dark:text-gray-100 mb-4">我的订单</h2>

      <!-- 订单列表表格 -->
      <table class="w-full text-sm border border-gray-300 dark:border-gray-700">
        <thead class="bg-gray-100 dark:bg-gray-700">
          <tr class="text-gray-900 dark:text-gray-100">
            <th class="border border-gray-300 dark:border-gray-700 px-3 py-2">订单编号</th>
            <th class="border border-gray-300 dark:border-gray-700 px-3 py-2">订单内容</th>
            <th class="border border-gray-300 dark:border-gray-700 px-3 py-2">下单时间</th>
            <th class="border border-gray-300 dark:border-gray-700 px-3 py-2">操作</th>
          </tr>
        </thead>
        <tbody class="text-gray-800 dark:text-gray-200">
          <tr
            v-for="order in orders"
            :key="order.id"
            class="hover:bg-gray-50 dark:hover:bg-gray-700"
          >
            <!-- 订单编号 -->
            <td class="border border-gray-300 dark:border-gray-700 px-3 py-2">
              {{ order.order_no }}
            </td>

            <!-- 订单内容明细 -->
            <td class="border border-gray-300 dark:border-gray-700 px-3 py-2">
              <ul class="space-y-1">
                <li
                  v-for="item in order.items"
                  :key="item.id"
                  class="text-gray-700 dark:text-gray-300"
                >
                  {{ item.name }} × {{ item.quantity }}
                </li>
              </ul>
            </td>

            <!-- 下单时间 -->
            <td class="border border-gray-300 dark:border-gray-700 px-3 py-2">
              {{ formatTime(order.created_at) }}
            </td>

            <!-- 删除按钮 -->
            <td class="border border-gray-300 dark:border-gray-700 px-3 py-2">
              <button
                class="px-3 py-1 text-xs bg-red-500 text-white rounded hover:bg-red-600 dark:hover:bg-red-400"
                @click="deleteOrder(order.id)"
              >
                删除订单
              </button>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- 空状态提示 -->
      <p v-if="orders.length === 0 && !loading" class="text-center text-gray-500 dark:text-gray-400 mt-4">
        暂无订单
      </p>

      <!-- 加载中提示 -->
      <p v-if="loading" class="text-center text-gray-500 dark:text-gray-400 mt-4">
        加载中...
      </p>

      <!-- 错误提示 -->
      <p v-if="error" class="text-red-500 text-xs mt-2">{{ error }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

// 这里可以改成你实际的用户 token 获取方式
const token = ref(localStorage.getItem('token') || '')
const orders = ref([])
const loading = ref(false)
const error = ref('')

// 格式化时间
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

// 获取用户订单列表
const fetchOrders = async () => {
  loading.value = true
  error.value = ''
  try {
    const res = await fetch('http://127.0.0.1:8000/orders/', {
      headers: {
        Authorization: `Bearer ${token.value}`
      }
    })
    if (res.ok) {
      orders.value = await res.json()
    } else {
      error.value = '获取订单失败'
    }
  } catch (err) {
    error.value = '网络错误，请稍后再试'
  } finally {
    loading.value = false
  }
}

// 删除订单
const deleteOrder = async (id) => {
  if (!confirm('确定要删除这个订单吗？')) return
  try {
    const res = await fetch(`http://127.0.0.1:8000/orders/${id}`, {
      method: 'DELETE',
      headers: {
        Authorization: `Bearer ${token.value}`
      }
    })
    if (res.ok) {
      // 直接从列表移除，减少一次请求
      orders.value = orders.value.filter(order => order.id !== id)
    } else {
      error.value = '删除订单失败'
    }
  } catch (err) {
    error.value = '网络错误，请稍后再试'
  }
}

onMounted(() => {
  if (!token.value) {
    // 未登录跳转到登录页，根据你的路由调整
    window.location.href = '/login'
    return
  }
  fetchOrders()
})
</script>