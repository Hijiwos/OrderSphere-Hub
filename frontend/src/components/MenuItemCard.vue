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
        :src="`http://127.0.0.1:8000${item.image_url}`"
        alt=""
        class="w-20 h-20 object-cover rounded cursor-pointer"
        @mouseenter="showTooltip = true"
        @mouseleave="showTooltip = false"
      />

      <!-- 右侧信息 -->
      <div class="flex-1 flex flex-col justify-between">
        <div>
          <h3
            class="text-lg font-semibold cursor-pointer"
            @mouseenter="showTooltip = true"
            @mouseleave="showTooltip = false"
          >
            {{ item.name }}
          </h3>
          <p class="text-gray-600">￥{{ item.price }}</p>
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
import { ref } from 'vue'
import BaseDialog from './BaseDialog.vue'

const props = defineProps({ item: Object })
const emits = defineEmits(['add'])

const quantity = ref(1)
const showTooltip = ref(false)
const dialogRef = ref(null)

const increase = () => quantity.value++
const decrease = () => { if (quantity.value > 1) quantity.value-- }

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
    // const result = await dialogRef.value.open({    // 是否需要保护函数？
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