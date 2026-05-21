<template>
  <div class="p-6">
    <h2 class="text-xl font-bold mb-4">运营配置</h2>
    <form @submit.prevent="saveSettings" class="space-y-4 max-w-md">
      <div>
        <label class="block mb-1">营业时间</label>
        <input v-model="settings.openTime" type="time" class="border rounded px-2 py-1" />
        <span> - </span>
        <input v-model="settings.closeTime" type="time" class="border rounded px-2 py-1" />
      </div>
      <div>
        <label class="block mb-1">税率 (%)</label>
        <input v-model.number="settings.taxRate" type="number" min="0" max="100" class="border rounded px-2 py-1" />
      </div>
      <div>
        <label class="block mb-1">送餐费 (元)</label>
        <input v-model.number="settings.deliveryFee" type="number" min="0" class="border rounded px-2 py-1" />
      </div>
      <div>
        <label class="block mb-1">默认语言</label>
        <select v-model="settings.language" class="border rounded px-2 py-1">
          <option value="zh-CN">简体中文</option>
          <option value="en-US">English</option>
        </select>
      </div>
      <div class="flex gap-2">
        <button type="submit" class="bg-green-600 text-white px-4 py-1 rounded">保存</button>
        <button type="button" class="bg-yellow-600 text-white px-4 py-1 rounded" @click="rollback">回滚</button>
        <button type="button" class="bg-blue-600 text-white px-4 py-1 rounded" @click="exportConfig">导出</button>
        <input type="file" class="hidden" ref="importInput" @change="importConfig" />
        <button type="button" class="bg-gray-600 text-white px-4 py-1 rounded" @click="triggerImport">导入</button>
      </div>
    </form>
    <div v-if="msg" class="mt-4 text-green-600">{{ msg }}</div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const defaultSettings = {
  openTime: '08:00',
  closeTime: '22:00',
  taxRate: 6,
  deliveryFee: 3,
  language: 'zh-CN'
}
const settings = ref({ ...defaultSettings })
const backup = ref({ ...defaultSettings })
const msg = ref('')
const importInput = ref(null)

function saveSettings() {
  // 实际应PUT /admin/settings
  backup.value = { ...settings.value }
  msg.value = '保存成功'
}
function rollback() {
  settings.value = { ...backup.value }
  msg.value = '已回滚到上次保存'
}
function exportConfig() {
  const blob = new Blob([JSON.stringify(settings.value, null, 2)], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = 'settings.json'
  a.click()
  URL.revokeObjectURL(url)
}
function triggerImport() {
  importInput.value.click()
}
function importConfig(e) {
  const file = e.target.files[0]
  if (!file) return
  const reader = new FileReader()
  reader.onload = () => {
    try {
      const data = JSON.parse(reader.result)
      settings.value = { ...settings.value, ...data }
      msg.value = '导入成功'
    } catch {
      msg.value = '导入失败，文件格式错误'
    }
  }
  reader.readAsText(file)
}
</script>
