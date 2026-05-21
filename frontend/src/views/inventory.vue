<template>
  <div class="max-w-5xl mx-auto mt-8 bg-white dark:bg-gray-800 p-6 rounded shadow">
    <h2 class="text-2xl font-bold mb-6 text-center">原料库存管理</h2>

    <div class="flex gap-3 mb-4 justify-center">
      <button @click="goTo('/admin/inventory/in')" class="btn-primary px-4">原料入库</button>
      <button @click="goTo('/admin/inventory/out')" class="btn-primary px-4 bg-orange-600">原料出库</button>
      <button @click="goTo('/admin/inventory/alerts')" class="btn-primary px-4 bg-red-600">库存预警</button>
    </div>

    <div class="overflow-x-auto">
      <table class="w-full text-sm">
        <thead>
          <tr class="bg-gray-100 dark:bg-gray-700">
            <th class="p-3 text-left">ID</th>
            <th class="p-3 text-left">原料名称</th>
            <th class="p-3 text-left">单位</th>
            <th class="p-3 text-left">当前库存</th>
            <th class="p-3 text-left">预警阈值</th>
            <th class="p-3 text-left">状态</th>
            <th class="p-3 text-left">操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in list" :key="item.id" class="border-t dark:border-gray-700">
            <td class="p-3">{{ item.id }}</td>
            <td class="p-3">{{ item.name }}</td>
            <td class="p-3">{{ item.unit }}</td>
            <td class="p-3 font-medium">{{ item.stock }}</td>
            <td class="p-3">{{ item.warn_threshold }}</td>
            <td class="p-3">
              <span :class="item.stock <= item.warn_threshold ? 'text-red-600' : 'text-green-600'">
                {{ item.stock <= item.warn_threshold ? '预警' : '正常' }}
              </span>
            </td>
            <td class="p-3 space-x-2">
              <button @click="editItem(item)" class="text-blue-600">编辑</button>
            </td>
          </tr>
          <tr v-if="list.length === 0">
            <td colspan="7" class="p-4 text-center text-gray-500">暂无原料</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 编辑弹窗 -->
    <div v-if="showModal" class="fixed inset-0 bg-black/40 flex items-center justify-center z-50">
      <div class="bg-white dark:bg-gray-800 p-6 rounded w-full max-w-md">
        <h3 class="text-xl font-bold mb-4">编辑原料</h3>
        <form @submit.prevent="updateItem">
          <div class="mb-3">
            <input v-model="form.name" class="input" placeholder="原料名称" readonly />
          </div>
          <div class="mb-3">
            <input v-model.number="form.warn_threshold" class="input" placeholder="预警阈值" required />
          </div>
          <div class="flex justify-end gap-2 mt-4">
            <button @click="showModal=false" type="button" class="px-3 py-1 border rounded">取消</button>
            <button type="submit" class="btn-primary px-3">保存</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
const router = useRouter()

const token = localStorage.getItem('token')
const list = ref([])
const showModal = ref(false)
const form = ref({})

const api = 'http://127.0.0.1:8000/admin/inventory'

async function getList() {
  const res = await fetch(api, {
    headers: { Authorization: `Bearer ${token}` }
  })
  list.value = await res.json()
}

function editItem(item) {
  form.value = { ...item }
  showModal.value = true
}

async function updateItem() {
  await fetch(`${api}/${form.value.id}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify(form.value)
  })
  showModal.value = false
  getList()
}

function goTo(path) {
  router.push(path)
}

onMounted(() => getList())
</script>

<style scoped>
.input {
  @apply w-full border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 p-2 rounded mb-2;
}
.btn-primary {
  @apply bg-blue-600 text-white py-2 rounded hover:bg-blue-700 transition;
}
</style>