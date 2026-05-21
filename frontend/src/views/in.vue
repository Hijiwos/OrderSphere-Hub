<template>
  <div class="max-w-md mx-auto mt-10 bg-white dark:bg-gray-800 p-6 rounded shadow">
    <h2 class="text-2xl font-bold mb-6 text-center">原料入库</h2>

    <form @submit.prevent="onSubmit" class="space-y-4">
      <div>
        <select v-model="form.material_id" class="input" required>
          <option value="">选择原料</option>
          <option v-for="item in materials" :key="item.id" :value="item.id">
            {{ item.name }} (库存：{{ item.stock }})
          </option>
        </select>
      </div>

      <div>
        <input v-model.number="form.quantity" type="number" min="0.01" step="0.01" class="input" placeholder="入库数量" required />
      </div>

      <div>
        <input v-model="form.remark" class="input" placeholder="备注（可选）" />
      </div>

      <button type="submit" class="btn-primary w-full">确认入库</button>

      <p v-if="success" class="text-green-600 text-sm text-center">{{ success }}</p>
      <p v-if="error" class="text-red-500 text-sm text-center">{{ error }}</p>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
const token = localStorage.getItem('token')

const materials = ref([])
const form = ref({ material_id: '', quantity: '', remark: '' })
const success = ref('')
const error = ref('')

async function getMaterials() {
  const res = await fetch('http://127.0.0.1:8000/admin/inventory', {
    headers: { Authorization: `Bearer ${token}` }
  })
  materials.value = await res.json()
}

async function onSubmit() {
  success.value = ''
  error.value = ''
  try {
    await fetch('http://127.0.0.1:8000/admin/inventory/in', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify(form.value)
    })
    success.value = '入库成功'
    form.value = { material_id: '', quantity: '', remark: '' }
  } catch (e) {
    error.value = '入库失败'
  }
}

onMounted(() => getMaterials())
</script>

<style scoped>
.input {
  @apply w-full border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 p-2 rounded mb-2;
}
.btn-primary {
  @apply w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 transition;
}
</style>