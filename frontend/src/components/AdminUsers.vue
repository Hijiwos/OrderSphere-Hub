<template>
  <div>
    <div class="flex items-center justify-between mb-3">
      <h2 class="text-lg font-bold">用户管理</h2>
    </div>

    <table class="w-full text-sm border">
      <thead class="bg-gray-100">
        <tr>
          <th class="border px-2 py-1">ID</th>
          <th class="border px-2 py-1">用户名</th>
          <th class="border px-2 py-1">是否管理员</th>
          <th class="border px-2 py-1">操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in users" :key="user.id">
          <td class="border px-2 py-1">{{ user.id }}</td>
          <td class="border px-2 py-1">{{ user.username }}</td>
          <td class="border px-2 py-1">
            <span
              class="px-2 py-1 text-xs rounded"
              :class="user.is_admin ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-600'"
            >
              {{ user.is_admin ? '是' : '否' }}
            </span>
          </td>
          <td class="border px-2 py-1 space-x-2">
            <button
              v-if="!user.is_admin"
              class="px-2 py-1 text-xs bg-blue-500 text-white rounded"
              @click="makeAdmin(user.id)"
            >
              设为管理员
            </button>
            <button
              class="px-2 py-1 text-xs bg-red-500 text-white rounded"
              @click="remove(user.id)"
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

const users = ref([])
const error = ref('')

const fetchUsers = async () => {
  error.value = ''
  const res = await fetch('http://127.0.0.1:8000/admin/users/', {
    headers: {
      Authorization: `Bearer ${props.token}`
    }
  })
  if (res.ok) {
    users.value = await res.json()
  } else {
    error.value = '获取用户失败'
  }
}

const remove = async (id) => {
  if (!confirm('确认删除该用户？')) return
  const res = await fetch(`http://127.0.0.1:8000/admin/users/${id}`, {
    method: 'DELETE',
    headers: {
      Authorization: `Bearer ${props.token}`
    }
  })
  if (res.ok) {
    await fetchUsers()
  } else {
    error.value = '删除失败'
  }
}

const makeAdmin = async (id) => {
  const res = await fetch(`http://127.0.0.1:8000/admin/users/${id}/make_admin`, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${props.token}`
    }
  })
  if (res.ok) {
    await fetchUsers()
  } else {
    error.value = '设置管理员失败'
  }
}

onMounted(fetchUsers)
watch(() => props.token, () => {
  if (props.token) fetchUsers()
})
</script>
