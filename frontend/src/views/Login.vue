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
  <BaseDialog ref="dialogRef" />
</template>

<script setup>
import { ref } from 'vue'
import api from '../api'
import { useUserStore } from '../store/user'
import { useRouter } from 'vue-router'
import BaseDialog from "../components/BaseDialog.vue";

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


    await showDialog(1500, 'lift', '在线点餐系统', 'left', '登录成功', 'center', undefined)
    // alert('登录成功')
    await router.push('/menu')
  } catch (e) {
    await showDialog(1500, 'lift', '在线点餐系统', 'left', '登录失败，请检查用户名或密码', 'center', undefined)
    // alert('登录失败，请检查用户名或密码')
  }
}

const dialogRef = ref(null)

const waitForDialog = (timeout = 2000) => {
  return new Promise((resolve, reject) => {
    const start = Date.now()
    const check = async () => {
      if (dialogRef.value && typeof dialogRef.value.open === 'function') {
        resolve(dialogRef.value)
      } else if (Date.now() - start > timeout) {
        reject(new Error('弹窗组件未就绪'))
      } else {
        await new Promise(r => setTimeout(r, 50))
        await check()
      }
    }
    check()
  })
}

const showDialog = async (duration=5000, titleAlign='lift', title='默认标题', messageAlign='left', message='默认信息', position='center', closeOnClickOverlay=undefined) => {
  try {
    const dialog = await waitForDialog()
    const result = await dialog.open({
      title: title,
      message: message,
      position: position,
      showButtons: false,
      closeOnClickOverlay: closeOnClickOverlay,
      duration: duration,
      titleAlign: titleAlign,
      messageAlign: messageAlign,
      overlay: false
    })
    console.log('dialog result:', result)
  } catch (error) {
    console.error('弹窗失败或超时', error)
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