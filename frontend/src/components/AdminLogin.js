import axios from 'axios'
export default {
  template: `
  <div class="container py-5 d-flex justify-content-center">
  <div class="w-100" style="max-width: 400px;">
    <h1 class="text-center mb-4">Sign In as an Admin</h1>
    <form @submit.prevent="loginAdmin" class="p-4 border rounded bg-light">
      <div class="mb-3">
        <label for="username" class="form-label">Username:</label>
        <input
          type="text"
          id="username"
          v-model="username"
          class="form-control"
          required
        />
      </div>
      <div class="mb-3">
        <label for="password" class="form-label">Password:</label>
        <input
          type="password"
          id="password"
          v-model="password"
          class="form-control"
          required
        />
      </div>
      <p
        v-if="message"
        class="text-danger text-center mb-3"
        id="warning-message"
      >
        {{ message }}
      </p>
      <div class="text-center">
        <button type="submit" class="btn btn-primary w-100">Login</button>
      </div>
    </form>
  </div>
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
    async loginAdmin () {
      try {
        await axios.post('/server/login', {
          username: this.username,
          password: this.password,
          role:'admin',
        }, { headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    },withCredentials: true })
        const response = await axios.get('/server/get_user', { withCredentials: true })
        const user = response.data
        localStorage.setItem('user', JSON.stringify(user))
        this.$router.push('/admin')
      } catch (error) {
        this.message='Login failed: ' + error.response.data.message
      }
    }
  }
}