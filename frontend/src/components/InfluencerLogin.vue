<template>
  <div>
    <h2>Influencer Login</h2>
    <form @submit.prevent="login">
      <input v-model="email" placeholder="Email" required />
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
      email: '',
      password: ''
    }
  },
  methods: {
    async login () {
      try {
        await axios.post('http://localhost:5000/influencer/login', {
          email: this.email,
          password: this.password
        }, { withCredentials: true })
        const response = await axios.get('http://localhost:5000/get_user', { withCredentials: true })
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
