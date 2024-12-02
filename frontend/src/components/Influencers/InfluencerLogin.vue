<template>
  <div>
    <h2>Influencer Login</h2>
    <form @submit.prevent="login">
      <input v-model="username" placeholder="Username" required />
      <input v-model="password" type="password" placeholder="Password" required />
      <button type="submit">Login</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data () {
    return {
      username: '',
      password: ''
    }
  },
  methods: {
    async login () {
      try {
        await axios.post('/server/login', {
          username: this.username,
          password: this.password,
          role:'influencer',
          }, {
          headers: {'Content-Type': 'application/x-www-form-urlencoded'},
          withCredentials: true 
        })
        const response = await axios.get('/server/get_user', { withCredentials: true })
        const user = response.data
        localStorage.setItem('user', JSON.stringify(user))
        this.$router.push('/influencer')
      } catch (error) {
        alert('Login failed: ' + error.response.data.message)
      }
    }
  }
}
</script>
