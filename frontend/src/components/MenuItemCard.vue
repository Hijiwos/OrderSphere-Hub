<template>
  <div class="relative">
    <div
      v-if="showTooltip"
      class="pointer-events-none absolute left-1/2 -translate-x-1/2 -top-3 -translate-y-full
             bg-black text-white text-xs px-3 py-2 rounded shadow-lg w-48
             opacity-90 animate-fade z-50"
    >
      {{ item.description }}
    </div>

    <div class="flex items-center bg-white dark:bg-gray-800 rounded shadow p-3 space-x-4">

      <!-- 左侧小图片 -->
      <img
        :src="item.image_url ? `http://127.0.0.1:8000${item.image_url}` : ''"
        alt=""
        class="w-20 h-20 object-cover rounded cursor-pointer"
        @mouseenter="showTooltip = true"
        @mouseleave="showTooltip = false"
      />

      <!-- 右侧信息 -->
      <div class="flex-1 flex flex-col justify-between">
        <div>
          <div class="flex items-center bg-white dark:bg-gray-800 p-3 w-full">
            <h3
              class="text-lg font-semibold cursor-pointer"
              @mouseenter="showTooltip = true"
              @mouseleave="showTooltip = false"
            >
              {{ item.name }}
            </h3>

            <!-- 仅在已登录用户显示收藏星星 -->
            <button v-if="isLoggedIn" @click="toggleFavorite" class="ml-auto focus:outline-none">
              <!-- SVG：未收藏时空心（fill='none'，stroke可见）；收藏时实心黄色 -->
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="w-6 h-6 transition-colors duration-200"
                :class="isFavorited ? 'text-yellow-400' : 'text-gray-400'"
                viewBox="0 0 24 24"
              >
                <path
                  :fill="isFavorited ? 'currentColor' : 'none'"
                  :stroke="isFavorited ? 'none' : 'currentColor'"
                  stroke-width="1.5"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  d="M11.48 3.499a.562.562 0 0 1 1.04 0l2.125 5.111a.563.563 0 0 0 .475.345l5.518.442c.499.04.701.663.321.988l-4.204 3.602a.563.563 0 0 0-.182.557l1.285 5.385a.562.562 0 0 1-.84.61l-4.725-2.885a.562.562 0 0 0-.586 0l-4.725 2.885a.562.562 0 0 1-.84-.61l1.285-5.385a.562.562 0 0 0-.182-.557l-4.204-3.602a.562.562 0 0 1 .321-.988l5.518-.442a.563.563 0 0 0 .475-.345L11.48 3.5z"
                />
              </svg>
            </button>
          </div>
          <p class="text-gray-500">￥{{ item.price }}</p>
        </div>
        <div class="flex items-center space-x-3 mt-2">
          <button @click="decrease" class="px-2 bg-gray-300 dark:bg-gray-600 rounded">-</button>
          <span class="font-semibold">{{ quantity }}</span>
          <button @click="increase" class="px-2 bg-gray-300 dark:bg-gray-600 rounded">+</button>
        </div>
        <button
          @click="add"
          class="mt-2 bg-green-600 text-white py-1 rounded text-sm"
        >
          加入购物车
        </button>
      </div>
    </div>

    <!-- 弹窗组件 -->
    <BaseDialog ref="dialogRef" />
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import BaseDialog from './BaseDialog.vue'
import api from '../api'
import { useUserStore } from '../store/user'

const props = defineProps({ item: Object })
const emits = defineEmits(['add'])

const quantity = ref(1)
const showTooltip = ref(false)
const dialogRef = ref(null)

const increase = () => quantity.value++
const decrease = () => { if (quantity.value > 1) quantity.value-- }

const user = useUserStore()
const isLoggedIn = computed(() => !!user.username)

// isFavorited reflects whether current user liked this item
const isFavorited = ref(false);

// initialize isFavorited when component mounts or when user.liked changes
watch(
  () => [user.liked, props.item && props.item.id],
  () => {
    try {
      const likedArr = Array.isArray(user.liked) ? user.liked : []
      isFavorited.value = likedArr.includes(props.item?.id)
    } catch (e) {
      isFavorited.value = false
    }
  },
  { immediate: true }
)

const toggleFavorite = async () => {
  if (!isLoggedIn.value) return

  const prev = Array.isArray(user.liked) ? [...user.liked] : []
  const id = props.item?.id
  if (id == null) return

  const next = prev.includes(id) ? prev.filter(x => x !== id) : [...prev, id]

  // Optimistic update
  user.setLiked(next)
  isFavorited.value = next.includes(id)

  try {
    // send array to backend
    await api.post('/users/me/liked', { liked: next })
  } catch (err) {
    console.error('保存收藏失败', err)
    // revert
    user.setLiked(prev)
    isFavorited.value = prev.includes(id)
  }
}

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

const showSimpleDialog = async () => {
  try {
    const dialog = await waitForDialog()
    const result = await dialog.open({
      title: '购物车',
      message: '已加入购物车：' + props.item.name + ' × ' + quantity.value,
      messageAlign: 'center',
      duration: 1000,
      overlay: false,
      position: 'top'
    })
    console.log('dialog result:', result)
  } catch (error) {
    console.error('弹窗失败或超时', error)
  }
}

const add = async () => {
  emits('add', { ...props.item, quantity: quantity.value })
  await showSimpleDialog()
  quantity.value = 1
}
</script>

<style scoped>
@keyframes fade {
  from { opacity: 0; transform: translate(-50%, -120%); }
  to { opacity: 1; transform: translate(-50%, -100%); }
}
.animate-fade { animation: fade 0.15s ease-out; }
</style>