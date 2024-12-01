<template>
  <div>
    <h2>Sponsor Login</h2>
    <form @submit.prevent="login">
      <input v-model="username" placeholder="Username" required />
      <input v-model="password" type="password" placeholder="Password" required />
      <button type="submit">Login</button>
    </form>
  </div>
  <div>
    <p> New user? <router-link to="/sponsor/register">Register here</router-link></p>
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
          role:'sponsor',
        }, { headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    },withCredentials: true })
        const response = await axios.get('/server/get_user', { withCredentials: true })
        const user = response.data
        localStorage.setItem('user', JSON.stringify(user))
        this.$router.push('/sponsor')
      } catch (error) {
        alert('Login failed: ' + error.response.data.message)
      }
    }
  }
}
</script>
