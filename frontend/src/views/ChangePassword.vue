<template>
  <div class="max-w-md mx-auto mt-10 bg-white dark:bg-gray-800 p-6 rounded shadow">
    <h2 class="text-2xl font-bold mb-4 text-center">修改密码</h2>

    <form @submit.prevent="onSubmit" class="space-y-4">
      <div>
        <input v-model="form.current_password" type="password" class="input" placeholder="当前密码" required />
      </div>

      <div>
        <input v-model="form.password" type="password" class="input" placeholder="新密码" required aria-describedby="password-strength" />
        <input v-model="form.confirm_password" type="password" class="input" placeholder="请再次输入新密码" required />
        <div class="mt-2">
          <div class="w-full bg-gray-200 h-2 rounded overflow-hidden">
            <div :style="{ width: passwordStrength.width }" :class="passwordStrength.colorClass" class="h-2 transition-all"></div>
          </div>
          <p id="password-strength" class="text-xs mt-1" :class="passwordStrength.textClass">{{ passwordStrength.text }}</p>
          <p v-if="isPasswordTooShort" class="text-xs mt-1 text-red-600">密码至少为6位</p>
        </div>
      </div>

      <p v-if="passwordMismatch" class="text-red-500 text-xs mt-1">两次输入的密码不一致</p>

      <div class="flex items-center justify-between">
        <button type="submit" class="btn-primary">保存修改</button>
      </div>

      <p v-if="success" class="text-green-600 text-sm mt-2">{{ success }}</p>
      <p v-if="error" class="text-red-500 text-sm mt-2">{{ error }}</p>
    </form>
  </div>
</template>

<script setup>
import { reactive, computed, ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const form = reactive({
  current_password: '',
  password: '',
  confirm_password: ''
})

function calcPasswordScore(pw) {
  if (!pw) return 0
  let raw = 0
  if (pw.length >= 6) raw++
  if (/[A-Za-z]/.test(pw) && /[0-9]/.test(pw)) raw++
  if (/[A-Z]/.test(pw) && /[a-z]/.test(pw)) raw++
  if (/[!@#$%^&*(),.?":{}|<>]/.test(pw)) raw++
  if (raw <= 1) return 0
  if (raw === 2) return 1
  if (raw === 3) return 2
  return 3
}

const passwordStrength = computed(() => {
  const pw = form.password
  if (!pw) return { width: '0%', colorClass: '', text: '', textClass: '', score: 0 }
  const score = calcPasswordScore(pw)
  const map = [
    { width: '33%', colorClass: 'bg-red-500', text: '弱', textClass: 'text-red-600' },
    { width: '66%', colorClass: 'bg-yellow-500', text: '中', textClass: 'text-yellow-600' },
    { width: '100%', colorClass: 'bg-green-500', text: '强', textClass: 'text-green-600' },
    { width: '100%', colorClass: 'bg-green-700', text: '非常强', textClass: 'text-green-700' }
  ]
  return { ...map[score], score }
})

const isPasswordTooShort = computed(() => form.password.length > 0 && form.password.length < 6)
const passwordMismatch = computed(() => form.confirm_password && form.password !== form.confirm_password)

const error = ref('')
const success = ref('')

async function onSubmit() {
  error.value = ''
  success.value = ''

  if (passwordMismatch.value) {
    error.value = '两次输入的密码不一致'
    return
  }
  const token = localStorage.getItem('token')
  if (!token) {
    error.value = '未登录'
    return
  }

  try {
    const res = await fetch('http://127.0.0.1:8000/users/me', {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify(form)
    })

    if (!res.ok) {
      const data = await res.json()
      error.value = data.detail || '更新失败'
      return
    }

    success.value = '更新成功'
    form.current_password = ''
    form.password = ''
    form.confirm_password = ''
    // 可选：返回资料页
    // router.push('/profile')
  } catch (e) {
    error.value = '网络错误'
  }
}
</script>

<style scoped>
.input {
  @apply w-full border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 p-2 rounded mb-3;
}
.btn-primary {
  @apply w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 transition;
}
</style>