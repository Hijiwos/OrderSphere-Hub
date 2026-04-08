<template>
  <div class="p-6 max-w-2xl mx-auto text-gray-900 dark:text-gray-100">
    <h1 class="text-2xl font-bold mb-4">购物车</h1>

    <div v-if="cart.items.length === 0" class="text-gray-600 dark:text-gray-400">
      购物车为空。
    </div>

    <div v-else class="space-y-4">

      <!-- 每个料理卡片 -->
      <div
        v-for="item in cart.items"
        :key="item.id"
        class="flex items-center bg-white dark:bg-gray-800 rounded shadow p-3 space-x-4"
      >

        <!-- 左侧小图标 -->
        <img
          :src="`http://127.0.0.1:8000${item.image_url}`"
          alt=""
          class="w-16 h-16 object-cover rounded"
        />

        <!-- 右侧信息 -->
        <div class="flex-1 flex justify-between items-center">

          <!-- 名称 + 价格 -->
          <div>
            <p class="font-semibold">{{ item.name }}</p>
            <p class="text-gray-600 dark:text-gray-400">￥{{ item.price }}</p>
          </div>

          <!-- 数量编辑 + 删除 -->
          <div class="flex items-center space-x-3">

            <button
              @click="cart.decrease(item)"
              class="qty-btn"
            >
              -
            </button>

            <span class="font-semibold">{{ item.quantity }}</span>

            <button
              @click="cart.increase(item)"
              class="qty-btn"
            >
              +
            </button>

            <button
              @click="cart.remove(item)"
              class="text-red-500 dark:text-red-400 hover:text-red-600 dark:hover:text-red-300 ml-4"
            >
              删除
            </button>

          </div>
        </div>
      </div>

      <!-- 总价 -->
      <div class="text-right text-xl font-bold mt-4">
        总价：￥{{ cart.totalPrice }}
      </div>

      <!-- 提交订单 -->
      <button
        @click="submitOrder"
        class="btn btn-primary w-full mt-4"
      >
        提交订单
      </button>
    </div>
    <BaseDialog ref="dialogRef" />
  </div>
</template>

<script setup>
import { useCartStore } from '../store/cart'
import { useUserStore } from '../store/user'
import BaseDialog from "../components/BaseDialog.vue";
import {ref} from "vue";

const cart = useCartStore()
const user = useUserStore()
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

const showDialog = async (showButtons=false, duration=5000, titleAlign='lift', title='默认标题', messageAlign='left', message='默认信息', position='center', closeOnClickOverlay=undefined) => {
  try {
    const dialog = await waitForDialog()
    const result = await dialog.open({
      title: title,
      message: message,
      position: position,
      showButtons: showButtons,
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

const submitOrder = async () => {
  if (cart.items.length === 0) {
    alert('购物车为空')
    return
  }

  const username = user.username
  const token = localStorage.getItem('token')

  if (!username || !token) {
    await showDialog(false, 1500, 'center', '未登录', 'center', '请先登录后再提交订单!!!', 'center', true)
    // alert('请先登录后再提交订单')
    return
  }

  const payload = {
    customer_name: username,
    items: cart.items.map(i => ({
      menu_item_id: i.id,
      quantity: i.quantity
    }))
  }

  const res = await fetch('http://127.0.0.1:8000/orders/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  })

  if (!res.ok) {
    await showDialog(false, 1500, 'center', '错误', 'center', '提交订单失败', 'center')
    // alert('提交订单失败')
    return
  }

  await showDialog(false, 1500, 'center', '谢谢惠顾', 'center', '订单提交成功', 'center', true)
  // alert('订单提交成功')
  cart.clear()
}
</script>

<style scoped>
.btn {
  @apply px-3 py-2 text-sm rounded transition-colors;
}
.btn-primary {
  @apply bg-green-600 text-white hover:bg-green-700;
}
.qty-btn {
  @apply px-3 py-1 rounded font-bold
         bg-gray-300 dark:bg-gray-600
         text-gray-800 dark:text-gray-100
         hover:bg-gray-400 dark:hover:bg-gray-500;
}
</style>
