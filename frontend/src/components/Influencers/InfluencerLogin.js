import axios from 'axios'
import { RouterLink } from 'vue-router';
export default {
  template: `
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
  `,
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