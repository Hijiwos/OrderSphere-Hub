import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => ({
    id: null,
    username: null,
    isAdmin: false,
    avatar: null,
    email: null,
    // 存储用户收藏的菜品 id 列表
    liked: []
  }),

  actions: {
    // setUser 接受 id, username, isAdmin, avatar, email, liked
    setUser(id, username, isAdmin, avatar = null, email = null, liked = []) {
      this.id = id
      this.username = username
      this.isAdmin = isAdmin
      this.avatar = avatar
      this.email = email
      this.liked = Array.isArray(liked) ? liked : []
    },

    setAvatar(avatarUrl) {
      this.avatar = avatarUrl
    },

    setLiked(likedArray) {
      this.liked = Array.isArray(likedArray) ? likedArray : []
    },

    logout() {
      this.id = null
      this.username = null
      this.isAdmin = false
      this.avatar = null
      this.email = null
      this.liked = []
      localStorage.removeItem('token')
    }
  }
})