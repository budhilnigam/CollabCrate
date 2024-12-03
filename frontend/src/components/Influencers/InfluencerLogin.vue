<template>
  <div class="login-container">
    <h1>Sign In as a Influencer</h1>
    <form @submit.prevent="loginInfluencer">
      <div class="login-form">
        <label for="username">Username:</label>
        <input
          type="text"
          id="username"
          v-model="username"
          required
        />
      </div>
      <div class="login-form">
        <label for="password">Password:</label>
        <input
          type="password"
          id="password"
          v-model="password"
          required
        />
      </div>
      <p v-if="message" class="warning" id="warning-message">{{ message }}</p>
      <button type="submit">Login</button>
    </form>
    <p class="text-center pt-2">Don't have an account? <RouterLink to="/influencer/register">Register</RouterLink></p>
  </div>
</template>

<script>
import axios from 'axios'
import { RouterLink } from 'vue-router';
export default {
  data () {
    return {
      username: '',
      password: '',
      message: ''
    }
  },
  methods: {
    async loginInfluencer () {
      try {
        await axios.post('/server/login', {
          username: this.username,
          password: this.password,
          role:'influencer',
        }, { headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    },withCredentials: true })
        const response = await axios.get('/server/get_user', { withCredentials: true })
        const user = response.data
        localStorage.setItem('user', JSON.stringify(user))
        this.$router.push('/influencer')
      } catch (error) {
        this.message='Login failed: ' + error.response.data.message
      }
    }
  }
}
</script>

<style scoped>
.login-container {
  max-width: 400px;
  margin: auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 10px;
  background-color: #f9f9f9;
}

h1 {
  text-align: center;
  margin-bottom: 20px;
}

.login-form {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
}

input {
  width: 100%;
  padding: 8px;
  box-sizing: border-box;
}

button {
  display: block;
  width: 100%;
  padding: 10px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}
</style>