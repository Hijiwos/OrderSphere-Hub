<template>
  <div class="max-w-3xl mx-auto mt-10 bg-white dark:bg-gray-800 p-6 rounded shadow">
    <h2 class="text-2xl font-bold mb-4 text-center">编辑个人资料</h2>

    <!-- 账户信息行（邮箱/登出/修改密码）- 简化展示 -->
    <div class="mb-6">
      <div class="flex items-center justify-between">
        <div>
          <div class="text-sm text-gray-600">登录邮箱</div>
          <div class="font-medium">{{ userEmail || '未设置' }}</div>
        </div>

        <div class="flex items-center space-x-3">
          <button @click="logout" class="bt_sml_defa">退出登录</button>
          <button @click="goChangePassword" class="bt_sml_defa">修改密码</button>
        </div>
      </div>
    </div>

    <form @submit.prevent="onSubmit" class="space-y-6">
      <!-- 用户名 显示 / 修改 布局（参考用户给出的格式） -->
      <table class="w-full">
        <tbody>
          <tr>
            <td style="padding-top:8px;text-align:right;width:25%" class="text-gray-700">
              用户名 :
            </td>
            <td style="padding-top:8px;text-align:left;width:75%">
              <!-- 显示模式 -->
              <div v-if="!editingNick" id="div_nickname_display">
                <span class="mr-4 font-medium">{{ username }}</span>
                <button type="button" class="bt_sml_defa" @click="dispNickChange">修改昵称</button>
              </div>

              <!-- 修改模式 -->
              <div v-else id="div_nickname_change">
                <input
                  v-model="tempNickname"
                  @input="onNickInput"
                  type="text"
                  name="nickname"
                  maxlength="32"
                  class="input_sml"
                  style="width:200px;"
                />
                <button type="button" @click="confirmNickChange" class="bt_sml_main ml-2">确认修改</button>
                <button type="button" @click="cancelNickChange" class="bt_sml_defa_narr ml-2">取消</button>

                <div class="mt-2">
                  <p v-if="checking" class="text-xs text-gray-500">检查中...</p>
                  <p v-else-if="tempNickname && nickAvailable === true" class="text-xs text-green-600">该用户名可用</p>
                  <p v-else-if="tempNickname && nickAvailable === false" class="text-xs text-red-600">该用户名已被占用</p>
                </div>
              </div>
            </td>
          </tr>
        </tbody>
      </table>

      <div>
        <p v-if="error" class="text-red-500 text-sm mt-2">{{ error }}</p>
        <p v-if="success" class="text-green-600 text-sm mt-2">{{ success }}</p>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../store/user'

// 简单防抖函数，避免外部依赖
function debounce(fn, wait = 300) {
  let timeout = null
  return function (...args) {
    if (timeout) clearTimeout(timeout)
    timeout = setTimeout(() => fn.apply(this, args), wait)
  }
}

const user = useUserStore()
const router = useRouter()

const username = ref(user.username || '')
const tempNickname = ref(username.value)
const editingNick = ref(false)
const nickAvailable = ref(null) // null unknown, true available, false taken
const checking = ref(false)
const error = ref('')
const success = ref('')

const userEmail = user.email || '' // 若 store 有 email 字段

async function checkNickname(name) {
  if (!name || name === user.username) {
    nickAvailable.value = null
    checking.value = false
    return
  }

  checking.value = true
  nickAvailable.value = null
  try {
    // 请根据后端实际接口调整 URL 与返回字段
    const res = await fetch(`http://127.0.0.1:8000/auth/check-username?username=${encodeURIComponent(name)}`)
    if (!res.ok) {
      nickAvailable.value = null
    } else {
      const data = await res.json()
      // 假设返回 { available: true/false }
      nickAvailable.value = !!data.available
    }
  } catch (e) {
    nickAvailable.value = null
  } finally {
    checking.value = false
  }
}

const debouncedNickCheck = debounce((val) => checkNickname(val), 400)

function dispNickChange() {
  tempNickname.value = username.value
  editingNick.value = true
  nickAvailable.value = null
  error.value = ''
  success.value = ''
}

function cancelNickChange() {
  editingNick.value = false
  tempNickname.value = username.value
  nickAvailable.value = null
  error.value = ''
  success.value = ''
}

async function confirmNickChange() {
  error.value = ''
  success.value = ''
  const newName = (tempNickname.value || '').trim()
  if (!newName) {
    error.value = '用户名不能为空'
    return
  }
  if (nickAvailable.value === false) {
    error.value = '用户名已被占用'
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
      body: JSON.stringify({ username: newName })
    })
    if (!res.ok) {
      const data = await res.json()
      error.value = data.detail || '更新失败'
      return
    }
    success.value = '用户名更新成功'
    username.value = newName
    user.username = newName
    editingNick.value = false
  } catch (e) {
    error.value = '网络错误'
  }
}

function onNickInput() {
  error.value = ''
  success.value = ''
  debouncedNickCheck(tempNickname.value.trim())
}

// 兼容原表单“保存用户名”按钮行为：提交时如果处于编辑状态，执行确认修改；否则不做额外操作
async function onSubmit() {
  if (editingNick.value) {
    await confirmNickChange()
  }
}

const goChangePassword = () => {
  router.push('/change-password')
}

const logout = () => {
  user.logout()
  window.location.href = '/'
}
</script>

<style scoped>
/* 基本样式，适配示例按钮类名以便直接替换原模板样式 */
.input_sml {
  @apply border border-gray-300 p-1 rounded;
}

.bt_sml_defa {
  @apply bg-gray-200 text-gray-800 py-1 px-3 rounded;
}
.bt_sml_defa_narr {
  @apply bg-gray-100 text-gray-800 py-1 px-3 rounded;
}
.bt_sml_main {
  @apply bg-blue-600 text-white py-1 px-3 rounded;
}

.btn-primary {
  @apply bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700 transition;
}
.btn-secondary {
  @apply bg-gray-300 text-gray-800 py-2 px-4 rounded hover:bg-gray-400 transition;
}
.btn-logout {
  @apply w-full bg-red-600 text-white py-2 rounded hover:bg-red-700 transition;
}
</style>