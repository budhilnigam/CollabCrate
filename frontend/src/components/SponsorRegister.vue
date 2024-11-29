<template>
  <div>
    <h2>Sponsor Registration</h2>
    <form @submit.prevent="register">
      <input v-model="email" placeholder="Email" required />
      <input v-model="password" type="password" placeholder="Password" required />
      <button type="submit">Register</button>
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
    async register () {
      try {
        await axios.post('http://localhost:5000/sponsor/register', {
          email: this.email,
          password: this.password
        })
        alert('Registration submitted. Awaiting admin approval.')
        this.$router.push('/sponsor/login')
      } catch (error) {
        alert('Registration failed: ' + error.response.data.message)
      }
    }
  }
}
</script>
