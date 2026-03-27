<template>
  <div>
    <h2 class="text-2xl font-bold mb-4 text-gray-900 dark:text-gray-100">菜单</h2>

    <!-- 搜索与筛选 -->
    <div class="bg-white dark:bg-gray-800 p-3 rounded shadow mb-5">

      <!-- 搜索行 -->
      <div class="flex gap-2 items-center">
        <input
          v-model="query"
          @keyup.enter="applyFilters"
          type="text"
          placeholder="按菜名模糊搜索（回车或点击搜索）"
          class="flex-1 input px-3 py-1"
        />

        <button
          @click="applyFilters"
          class="btn-primary px-3 py-1 text-sm"
        >
          搜索
        </button>

        <button
          @click="resetFilters"
          class="px-3 py-1 text-sm bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-100 rounded hover:bg-gray-300 dark:hover:bg-gray-600"
        >
          重置
        </button>
      </div>

      <!-- 类型 -->
      <div class="mt-4">
        <h3 class="text-sm font-semibold mb-2 text-gray-700 dark:text-gray-300">类型</h3>
        <div class="flex flex-wrap gap-2">
          <button
            v-for="t in types"
            :key="t"
            @click="toggleType(t)"
            :class="chipClass(selectedTypes.has(t), 'blue')"
            class="text-xs"
          >
            {{ t }}
          </button>
        </div>
      </div>

      <!-- 类别（分组） -->
      <div class="mt-4">
        <h3 class="text-sm font-semibold mb-2 text-gray-700 dark:text-gray-300">类别</h3>

        <div class="space-y-3">
          <div
            v-for="(groupItems, groupName) in groupedCategories"
            :key="groupName"
          >
            <div class="text-xs text-gray-600 dark:text-gray-400 mb-1">{{ groupName }}</div>

            <div class="flex flex-wrap gap-2">
              <button
                v-for="c in groupItems"
                :key="c"
                @click="toggleCategory(c)"
                :class="chipClass(selectedCategories.has(c), 'green')"
                class="text-xs"
              >
                {{ c }}
              </button>
            </div>
          </div>
        </div>
      </div>

    </div>

    <!-- 菜单展示 -->
    <div v-if="loading" class="text-center py-10 text-gray-700 dark:text-gray-300">正在加载菜单...</div>

    <div v-else>
      <div v-if="displayedMenu.length === 0" class="text-center text-gray-500 dark:text-gray-400 py-10">
        未找到符合条件的料理
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        <MenuItemCard
          v-for="item in displayedMenu"
          :key="item.id ?? item.name"
          :item="item"
          @add="addToCart"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import api from '../api'
import MenuItemCard from '../components/MenuItemCard.vue'
import { useCartStore } from '../store/cart'

const menu = ref([])
const displayedMenu = ref([])
const loading = ref(true)
const query = ref('')

const types = ref([])
const categories = ref([])
const selectedTypes = ref(new Set())
const selectedCategories = ref(new Set())

const cart = useCartStore()

function toArray(val) {
  if (!val && val !== 0) return []
  if (Array.isArray(val)) return val.filter(Boolean).map(v => String(v).trim())
  if (typeof val === 'string') {
    const s = val.trim()
    try {
      const p = JSON.parse(s)
      if (Array.isArray(p)) return p.map(v => String(v).trim()).filter(Boolean)
    } catch (e) {}
    return s.split(/[,;，、|/\\]/).map(x => x.trim()).filter(Boolean)
  }
  return [String(val).trim()]
}

function extractFieldArray(item, candidates) {
  for (const key of candidates) {
    if (key in item && item[key] != null) {
      return toArray(item[key])
    }
  }
  return []
}

const categoryGroups = {
  '恢复类': ['恢复血量', '持续恢复', '复活'],
  '攻击类': ['提升伤害', '提升攻击', '提升暴击', '提升暴击伤害'],
  '冒险类': ['恢复体力', '减少体力消耗', '减少严寒消耗', '环境交互恢复'],
  '防御类': ['提升防御', '提升护盾', '生命上限提升', '提升治疗效果', '元素充能效率提升'],
  '其他': ['其他', '不可制作']
}

const groupedCategories = computed(() => {
  const result = {}
  for (const [group, items] of Object.entries(categoryGroups)) {
    result[group] = items.filter(c => categories.value.includes(c))
  }
  return result
})

onMounted(async () => {
  try {
    const res = await api.get('/menu/')
    menu.value = res.data || []
    displayedMenu.value = menu.value.slice()

    const tSet = new Set()
    const cSet = new Set()

    for (const item of menu.value) {
      const itypes = extractFieldArray(item, ['type', 'types', 'food_type'])
      const icats = extractFieldArray(item, ['category', 'categories', 'food_category'])

      itypes.forEach(t => t && tSet.add(t))
      icats.forEach(c => c && cSet.add(c))
    }

    types.value = Array.from(tSet).sort((a, b) => a.localeCompare(b))
    categories.value = Array.from(cSet).sort((a, b) => a.localeCompare(b))

  } catch (err) {
    console.error('加载菜单失败', err)
  } finally {
    loading.value = false
  }
})

function toggleType(t) {
  const s = new Set(selectedTypes.value)
  s.has(t) ? s.delete(t) : s.add(t)
  selectedTypes.value = s
  applyFilters()
}

function toggleCategory(c) {
  const s = new Set(selectedCategories.value)
  s.has(c) ? s.delete(c) : s.add(c)
  selectedCategories.value = s
  applyFilters()
}

function resetFilters() {
  query.value = ''
  selectedTypes.value = new Set()
  selectedCategories.value = new Set()
  displayedMenu.value = menu.value.slice()
}

function applyFilters() {
  const q = (query.value || '').trim().toLowerCase()
  const selTypes = selectedTypes.value
  const selCats = selectedCategories.value

  displayedMenu.value = menu.value.filter(item => {
    const nameCandidates = ['name', 'title', 'foodName']
    let name = ''
    for (const k of nameCandidates) {
      if (k in item && item[k]) { name = String(item[k]); break }
    }
    if (q && !name.toLowerCase().includes(q)) return false

    if (selTypes.size > 0) {
      const itypes = extractFieldArray(item, ['type', 'types', 'food_type'])
      if (!itypes.some(t => selTypes.has(t))) return false
    }

    if (selCats.size > 0) {
      const icats = extractFieldArray(item, ['category', 'categories', 'food_category'])
      if (!icats.some(c => selCats.has(c))) return false
    }

    return true
  })
}

function addToCart(payload) {
  cart.add(payload)
}

function chipClass(selected, color) {
  const base =
      'px-2 py-0.5 rounded-full border transition-colors ' +
      'bg-white dark:bg-gray-700 text-gray-700 dark:text-gray-200 border-gray-300 dark:border-gray-600'

  if (selected) {
    if (color === 'blue')
      return `${base} bg-blue-600 text-white border-blue-600 hover:bg-blue-700`
    if (color === 'green')
      return `${base} bg-green-600 text-white border-green-600 hover:bg-green-700`
    return `${base} bg-gray-700 text-white border-gray-700`
  }

  return `${base} hover:bg-gray-100 dark:hover:bg-gray-600`
}
</script>

<style scoped>
.input {
  @apply w-full border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 p-2 rounded;
}

.btn-primary {
  @apply bg-blue-600 text-white py-2 rounded hover:bg-blue-700;
}

.flex::-webkit-scrollbar {
  height: 6px;
}
</style>
