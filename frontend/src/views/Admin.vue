<template>
  <div class="min-h-screen bg-gray-100">
    <header class="bg-white shadow px-6 py-4 flex items-center justify-between">
      <h1 class="text-xl font-bold">管理后台</h1>
      <div class="space-x-3">
        <span class="text-sm text-gray-600">管理员：{{ user.username || '未知' }}</span>

        <router-link
          to="/"
          class="text-sm text-blue-600 hover:underline"
        >
          返回前台
        </router-link>
      </div>
    </header>

    <main class="max-w-6xl mx-auto mt-6 bg-white rounded shadow p-4">
      <div class="flex border-b mb-4">
        <button
          v-for="tab in tabs"
          :key="tab.key"
          @click="currentTab = tab.key"
          class="px-4 py-2 -mb-px border-b-2"
          :class="currentTab === tab.key ? 'border-green-600 text-green-600' : 'border-transparent text-gray-500'"
        >
          {{ tab.label }}
        </button>
      </div>

      <section v-if="currentTab === 'menu'">
        <AdminMenu :token="token" />
      </section>

      <section v-else-if="currentTab === 'orders'">
        <AdminOrders :token="token" />
      </section>

      <section v-else-if="currentTab === 'users'">
        <AdminUsers :token="token" />
      </section>
    </main>
  </div>
</template>

<script setup>
import {useUserStore} from '../store/user'
import { ref, onMounted } from 'vue'
import AdminMenu from '../components/AdminMenu.vue'
import AdminOrders from '../components/AdminOrders.vue'
import AdminUsers from '../components/AdminUsers.vue'

const user = useUserStore()

const tabs = [
  { key: 'menu', label: '菜单管理' },
  { key: 'orders', label: '订单管理' },
  { key: 'users', label: '用户管理' }
]

const currentTab = ref('menu')

// ⭐ 使用管理员 token
const token = ref(localStorage.getItem('token') || '')
const username = ref(localStorage.getItem('username') || '')

onMounted(() => {
  if (!token.value) {
    window.location.href = '/login'
  }
})

</script>
