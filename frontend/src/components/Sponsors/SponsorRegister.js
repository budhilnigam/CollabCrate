import axios from 'axios';

export default {
  template: `
  <div class="container py-5" style="max-width: 500px;">
  <h1 class="text-center mb-4">Register as a Sponsor</h1>
  <form @submit.prevent="registerSponsor" class="p-4 border rounded bg-light">
    <div class="mb-3">
      <label for="username" class="form-label">Username:</label>
      <input
        type="text"
        id="username"
        v-model="formData.username"
        class="form-control"
        required
      />
    </div>
    <div class="mb-3">
      <label for="email" class="form-label">Email:</label>
      <input
        type="email"
        id="email"
        v-model="formData.email"
        class="form-control"
        required
      />
    </div>
    <div class="mb-3">
      <label for="password" class="form-label">Password:</label>
      <input
        type="password"
        id="password"
        v-model="formData.password"
        class="form-control"
        required
      />
    </div>
    <div class="mb-3">
      <label for="sp_industry" class="form-label">Industry:</label>
      <input
        type="text"
        id="sp_industry"
        v-model="formData.sp_industry"
        class="form-control"
        required
      />
    </div>
    <div class="mb-3">
      <label for="sp_budget" class="form-label">Budget:</label>
      <input
        type="number"
        id="sp_budget"
        v-model="formData.sp_budget"
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
      <button type="submit" class="btn btn-primary">Register</button>
    </div>
  </form>
  <p class="text-center pt-3">
    Already have an account?
    <RouterLink to="/sponsor/login" class="text-decoration-none">Sign In</RouterLink>
  </p>
</div>`,
  data() {
    return {
      formData: {
        username: '',
        email: '',
        password: '',
        sp_industry: '',
        sp_budget: ''
      },
      message: ''
    };
  },
  methods: {
    async registerSponsor() {
      try {
        const response = await axios.post('/server/register?role=sponsor', {
          username: this.formData.username,
          email: this.formData.email,
          password: this.formData.password,
          sp_industry: this.formData.sp_industry,
          sp_budget: this.formData.sp_budget
        },{headers: {
      'Content-Type': 'application/x-www-form-urlencoded'},withCredentials: true });
        this.message =
          response.data.message === true
            ? 'Registration successful!'
            : response.data.message;
            const user_data_response = await axios.get('/server/get_user', { withCredentials: true })
        const user = user_data_response.data
        localStorage.setItem('user', JSON.stringify(user))
        this.$router.push('/sponsor')
      } catch (error) {
        this.message = 'An error occurred during registration.'+error.response.data.message;
      }
    }
  }
};