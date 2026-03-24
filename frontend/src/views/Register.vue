<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-100 dark:bg-gray-900">
    <div class="w-full max-w-md bg-white dark:bg-gray-800 rounded shadow p-6">
      <h2 class="text-2xl font-bold mb-4 text-center">注册</h2>

      <form @submit.prevent="onSubmit" class="space-y-4">
        <div>
          <label class="block text-sm font-medium mb-1">用户名</label>
          <input
            v-model="form.username"
            type="text"
            class="input"
            required
          />
        </div>

        <div>
          <label class="block text-sm font-medium mb-1">密码</label>
          <input
            v-model="form.password"
            type="password"
            class="input"
            required
            aria-describedby="password-strength"
          />

          <!-- 密码复杂度进度条 -->
          <div class="mt-2">
            <div class="w-full bg-gray-200 h-2 rounded overflow-hidden">
              <div
                :style="{ width: passwordStrength.width }"
                :class="passwordStrength.colorClass"
                class="h-2 transition-all"
                role="progressbar"
                :aria-valuenow="passwordStrength.score"
                aria-valuemin="0"
                aria-valuemax="3"
              ></div>
            </div>
            <p id="password-strength" class="text-xs mt-1" :class="passwordStrength.textClass">
              {{ passwordStrength.text }}
            </p>
            <p v-if="isPasswordTooShort" class="text-xs mt-1 text-red-600">密码至少为6位</p>
          </div>
        </div>

        <div>
          <label class="block text-sm font-medium mb-1">确认密码</label>
          <input
            v-model="form.confirm_password"
            type="password"
            class="input"
            required
          />
          <p v-if="passwordMismatch" class="text-red-500 text-xs mt-1">
            两次输入的密码不一致
          </p>
        </div>

        <div class="flex items-center justify-between">
          <button
            type="submit"
            class="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 transition"
          >
            注册
          </button>
        </div>

        <p class="text-center text-sm mt-3">
          已有账号？
          <router-link to="/login" class="text-blue-600 hover:underline">去登录</router-link>
        </p>
      </form>
    </div>
  </div>
</template>

<script setup>
import { reactive, computed } from 'vue'

const form = reactive({
  username: '',
  password: '',
  confirm_password: ''
})

// 密码强度计算（你之前要求的均匀分布版本）
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

  // ⭐ 密码为空 → 返回“空状态”
  if (!pw) {
    return {
      width: '0%',
      colorClass: '',
      text: '',
      textClass: '',
      score: 0
    }
  }

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

function onSubmit() {
  if (passwordMismatch.value) {
    alert('两次密码不一致')
    return
  }

  alert('注册成功（你可以在这里接后端 API）')
}
</script>

<style scoped>
.input {
  @apply w-full p-2 border rounded dark:bg-gray-700 dark:text-white;
}
</style>
