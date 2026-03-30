<template>
  <div class="max-w-md mx-auto mt-10 bg-white dark:bg-gray-800 p-6 rounded shadow">
    <h2 class="text-2xl font-bold mb-4 text-center">登录</h2>

    <input v-model="username" class="input" placeholder="用户名" />
    <input v-model="password" type="password" class="input" placeholder="密码" />

    <button @click="login" class="btn-primary w-full mt-4">登录</button>

    <p class="text-center mt-4 text-sm">
      没有账号？
      <router-link to="/register" class="text-blue-500">注册</router-link>
    </p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import api from '../api'
import { useUserStore } from '../store/user'
import { useRouter } from 'vue-router'

const username = ref('')
const password = ref('')
const userStore = useUserStore()
const router = useRouter()

const login = async () => {
  try {
    const res = await api.post('/auth/login', {
      username: username.value,
      password: password.value
    })

    localStorage.setItem('token', res.data.access_token)
    // 从返回的 token payload 或直接返回的 avatar 字段恢复头像
    let avatar = null
    try {
      const payload = JSON.parse(atob(res.data.access_token.split('.')[1]))
      avatar = payload.avatar || res.data.avatar || null
      userStore.setUser(payload.sub, payload.is_admin, avatar)
    } catch (e) {
      // 如果解析 token 失败，退而使用服务端返回的 avatar 字段
      userStore.setUser(res.data.username, res.data.is_admin, res.data.avatar || null)
    }

    alert('登录成功')
    await router.push('/menu')
  } catch (e) {
    alert('登录失败，请检查用户名或密码')
  }
}
</script>

<style scoped>
.input {
  @apply w-full border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 p-2 rounded mb-3;
}
.btn-primary {
  @apply bg-blue-600 text-white py-2 rounded hover:bg-blue-700;
}
</style>