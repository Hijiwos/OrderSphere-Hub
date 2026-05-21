<template>
  <nav class="bg-gray-900 text-white px-4 sm:px-6 py-3 flex justify-between items-center">
    <h1 class="text-lg sm:text-xl font-bold">OrderSphere-Hub</h1>

    <div class="flex items-center space-x-3 sm:space-x-4 text-sm sm:text-base">
      <router-link to="/help" class="hover:text-blue-300">帮助</router-link>
      <router-link v-if="user.username" to="/menu" class="hover:text-blue-300">我的订单</router-link>
      <router-link to="/menu" class="hover:text-blue-300">菜单</router-link>
      <router-link to="/checkout" class="hover:text-blue-300">购物车</router-link>

      <router-link v-if="!user.username" to="/login" class="hover:text-blue-300">
        登录
      </router-link>

      <span v-else class="flex items-center space-x-2">
        <router-link to="/profile" class="flex items-center hover:text-blue-300 space-x-2">
          <img :src="avatarUrl" alt="avatar" class="w-8 h-8 rounded-full object-cover" />
          <span>{{ user.username }}</span>
        </router-link>
        <!-- 退出按钮已从这里移除；个人资料页有退出按钮 -->
      </span>

      <router-link v-if="user.isAdmin" to="/admin-dashboard" class="hover:text-yellow-300">
        管理员页面
      </router-link>

      <router-link v-if="user.isAdmin" to="/admin" class="hover:text-yellow-300">
        管理后台
      </router-link>

      <button @click="toggleDark" class="ml-2 text-yellow-300 hover:text-yellow-200">
        {{ dark ? '☀️' : '🌙' }}
      </button>
    </div>
  </nav>
</template>

<script setup>
import {ref, computed} from 'vue'
import {useUserStore} from '../store/user'

const user = useUserStore()
const dark = ref(false)

// Generate same default color avatar as profile to keep consistent look
function nameColorSeed(name) {
  let h = 0
  for (let i = 0; i < name.length; i++) {
    h = (h << 5) - h + name.charCodeAt(i)
    h |= 0
  }
  const r = (h & 0xff0000) >> 16
  const g = (h & 0x00ff00) >> 8
  const b = h & 0x0000ff
  return {r: (r + 200) % 256, g: (g + 120) % 256, b: (b + 40) % 256}
}

function generateColorAvatarDataUrl(name, size = 100) {
  const {r, g, b} = nameColorSeed(name || 'U')
  const canvas = document.createElement('canvas')
  canvas.width = size
  canvas.height = size
  const ctx = canvas.getContext('2d')
  ctx.fillStyle = `rgb(${r}, ${g}, ${b})`
  ctx.fillRect(0, 0, size, size)
  if (name && name.length) {
    const letter = name.trim()[0].toUpperCase()
    ctx.fillStyle = 'rgba(255,255,255,0.95)'
    ctx.font = `${Math.floor(size * 0.5)}px sans-serif`
    ctx.textAlign = 'center'
    ctx.textBaseline = 'middle'
    ctx.fillText(letter, size / 2, size / 2)
  }
  return canvas.toDataURL('image/png')
}

const avatarUrl = computed(() => {
  if (user.avatar) return `http://127.0.0.1:8000${user.avatar}`
  return generateColorAvatarDataUrl(user.username || 'U', 100)
})

let toggleDark = () => {
  document.documentElement.classList.toggle('dark')
  dark.value = !dark.value
}
</script>

<style scoped>
/* avatar styled via classes */
</style>