<template>
  <nav class="bg-gray-900 text-white px-4 sm:px-6 py-3 flex justify-between items-center">
    <h1 class="text-lg sm:text-xl font-bold">OrderSphere-Hub</h1>

    <div class="flex items-center space-x-3 sm:space-x-4 text-sm sm:text-base">
      <router-link to="/menu" class="hover:text-blue-300">菜单</router-link>
      <router-link to="/checkout" class="hover:text-blue-300">购物车</router-link>

      <router-link v-if="!user.username" to="/login" class="hover:text-blue-300">
        登录
      </router-link>

      <span v-else class="flex items-center space-x-2">
        <span>{{ user.username }}</span>
        <button @click="logout" class="text-red-400 hover:text-red-300">退出</button>
      </span>

      <router-link v-if="user.isAdmin" to="/admin" class="hover:text-yellow-300">
        管理后台
      </router-link>

      <button @click="toggleDark" class="ml-2 text-yellow-300 hover:text-yellow-200">
        🌙
      </button>
    </div>
  </nav>
</template>

<script setup>
import {useUserStore} from '../store/user'

const user = useUserStore()

const logout = () => {
  user.logout()
  window.location.href = '/'
}

const toggleDark = () => {
  document.documentElement.classList.toggle('dark')
}
</script>
