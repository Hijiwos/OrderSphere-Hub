<template>
  <div class="min-h-screen bg-gray-100 dark:bg-gray-900 py-8">
    <div class="max-w-3xl mx-auto bg-white dark:bg-gray-800 rounded-lg shadow p-6">
      <h2 class="text-2xl font-bold text-center text-gray-900 dark:text-white mb-6">使用帮助</h2>
      <!-- 使用说明文案 -->
      <p class="text-gray-700 dark:text-gray-300 leading-relaxed mb-8">
        本点餐系统区分普通用户与管理员双权限体系，普通用户无需注册即可浏览菜品、加入购物车、提交订单并管理个人订单；支持JSON批量导入菜单、统一管理菜品与全部订单，系统可实时核算消费金额、生成专属订单编号，前后端接口稳定适配，操作简单便捷，满足日常点餐与后台运维全部需求。
      </p>

      <!-- 问题反馈按钮 -->
      <div class="text-center">
        <router-link to="/feedback" class="px-6 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 inline-block">
        问题反馈
      </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>

</script>