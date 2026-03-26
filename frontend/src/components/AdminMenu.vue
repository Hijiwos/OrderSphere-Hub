<template>
  <div>
    <div class="flex items-center justify-between mb-3">
      <h2 class="text-lg font-bold">菜单管理</h2>
      <button
        class="px-3 py-1 bg-green-600 text-white rounded text-sm"
        @click="openCreate"
      >
        新增菜品
      </button>
    </div>

    <table class="w-full text-sm border">
      <thead class="bg-gray-100">
        <tr>
          <th class="border px-2 py-1">ID</th>
          <th class="border px-2 py-1">名称</th>
          <th class="border px-2 py-1">价格</th>
          <th class="border px-2 py-1">分类</th>
          <th class="border px-2 py-1">类型</th>
          <th class="border px-2 py-1">操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in items" :key="item.id">
          <td class="border px-2 py-1">{{ item.id }}</td>
          <td class="border px-2 py-1">{{ item.name }}</td>
          <td class="border px-2 py-1">{{ item.price }}</td>
          <td class="border px-2 py-1">{{ item.category }}</td>
          <td class="border px-2 py-1">{{ item.type }}</td>
          <td class="border px-2 py-1 space-x-2">
            <button
              class="px-2 py-1 text-xs bg-blue-500 text-white rounded"
              @click="openEdit(item)"
            >
              编辑
            </button>
            <button
              class="px-2 py-1 text-xs bg-red-500 text-white rounded"
              @click="remove(item.id)"
            >
              删除
            </button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- 简单弹窗 -->
    <div
      v-if="showDialog"
      class="fixed inset-0 bg-black/40 flex items-center justify-center"
    >
      <div class="bg-white rounded shadow p-4 w-full max-w-md">
        <h3 class="text-lg font-bold mb-3">
          {{ editingId ? '编辑菜品' : '新增菜品' }}
        </h3>

        <div class="space-y-2">
          <div>
            <label class="block text-xs mb-1">名称</label>
            <input v-model="form.name" class="w-full border rounded px-2 py-1" />
          </div>
          <div>
            <label class="block text-xs mb-1">价格</label>
            <input v-model.number="form.price" type="number" class="w-full border rounded px-2 py-1" />
          </div>
          <div>
            <label class="block text-xs mb-1">分类</label>
            <input v-model="form.category" class="w-full border rounded px-2 py-1" />
          </div>
          <div>
            <label class="block text-xs mb-1">类型</label>
            <input v-model="form.type" class="w-full border rounded px-2 py-1" />
          </div>
          <div>
            <label class="block text-xs mb-1">描述</label>
            <textarea v-model="form.description" class="w-full border rounded px-2 py-1" />
          </div>
        </div>

        <div class="mt-4 flex justify-end space-x-2">
          <button class="px-3 py-1 text-sm" @click="closeDialog">取消</button>
          <button
            class="px-3 py-1 text-sm bg-green-600 text-white rounded"
            @click="save"
          >
            保存
          </button>
        </div>

        <p v-if="error" class="text-red-500 text-xs mt-2">{{ error }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'

const props = defineProps({
  token: { type: String, required: true }
})

const items = ref([])
const showDialog = ref(false)
const editingId = ref(null)
const error = ref('')

const form = ref({
  name: '',
  price: 0,
  category: '',
  type: '',
  description: '',
  region: '',
  raw_key: '',
  image_url: ''
})

const fetchMenu = async () => {
  const res = await fetch('http://127.0.0.1:8000/admin/menu/', {
    headers: {
      Authorization: `Bearer ${props.token}`
    }
  })
  if (res.ok) {
    items.value = await res.json()
  }
}

const openCreate = () => {
  editingId.value = null
  form.value = {
    name: '',
    price: 0,
    category: '',
    type: '',
    description: '',
    region: '',
    raw_key: '',
    image_url: ''
  }
  showDialog.value = true
}

const openEdit = (item) => {
  editingId.value = item.id
  form.value = { ...item }
  showDialog.value = true
}

const closeDialog = () => {
  showDialog.value = false
  error.value = ''
}

const save = async () => {
  error.value = ''
  const method = editingId.value ? 'PUT' : 'POST'
  const url = editingId.value
    ? `http://127.0.0.1:8000/admin/menu/${editingId.value}`
    : 'http://127.0.0.1:8000/admin/menu/'

  const res = await fetch(url, {
    method,
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${props.token}`
    },
    body: JSON.stringify(form.value)
  })

  if (!res.ok) {
    const data = await res.json().catch(() => ({}))
    error.value = data.detail || '保存失败'
    return
  }

  closeDialog()
  await fetchMenu()
}

const remove = async (id) => {
  if (!confirm('确认删除该菜品？')) return
  const res = await fetch(`http://127.0.0.1:8000/admin/menu/${id}`, {
    method: 'DELETE',
    headers: {
      Authorization: `Bearer ${props.token}`
    }
  })
  if (res.ok) {
    await fetchMenu()
  }
}

onMounted(fetchMenu)
watch(() => props.token, () => {
  if (props.token) fetchMenu()
})
</script>
