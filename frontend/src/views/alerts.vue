<template>
  <div class="max-w-5xl mx-auto mt-8 bg-white dark:bg-gray-800 p-6 rounded shadow">
    <h2 class="text-2xl font-bold mb-6 text-center text-red-600">库存预警</h2>

    <div class="overflow-x-auto">
      <table class="w-full text-sm">
        <thead>
          <tr class="bg-red-50 dark:bg-red-900">
            <th class="p-3 text-left">原料</th>
            <th class="p-3 text-left">单位</th>
            <th class="p-3 text-left">当前库存</th>
            <th class="p-3 text-left">预警阈值</th>
            <th class="p-3 text-left">状态</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in list" :key="item.id" class="border-t dark:border-gray-700">
            <td class="p-3 font-medium">{{ item.name }}</td>
            <td class="p-3">{{ item.unit }}</td>
            <td class="p-3 text-red-600 font-bold">{{ item.stock }}</td>
            <td class="p-3">{{ item.warn_threshold }}</td>
            <td class="p-3 text-red-600 font-bold">库存不足</td>
          </tr>
          <tr v-if="list.length === 0">
            <td colspan="5" class="p-4 text-center text-green-600">全部原料库存正常</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
const token = localStorage.getItem('token')
const list = ref([])

async function getAlerts() {
  const res = await fetch('http://127.0.0.1:8000/admin/inventory/alerts', {
    headers: { Authorization: `Bearer ${token}` }
  })
  list.value = await res.json()
}

onMounted(() => getAlerts())
</script>

<style scoped>
.input {
  @apply w-full border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 p-2 rounded mb-2;
}
</style>