import axios from 'axios';

export default {
  template:`
  <div class="container py-5" style="max-width: 500px;">
  <h1 class="text-center mb-4">Register as an Influencer</h1>
  <form @submit.prevent="registerInfluencer" class="p-4 border rounded bg-light">
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
      <label for="inf_category" class="form-label">Category:</label>
      <input
        type="text"
        id="inf_category"
        v-model="formData.inf_category"
        class="form-control"
        required
      />
    </div>
    <div class="mb-3">
      <label for="inf_niche" class="form-label">Niche:</label>
      <input
        type="text"
        id="inf_niche"
        v-model="formData.inf_niche"
        class="form-control"
        required
      />
    </div>
    <div class="mb-3">
      <label for="inf_reach" class="form-label">Reach:</label>
      <input
        type="number"
        id="inf_reach"
        v-model="formData.inf_reach"
        class="form-control"
        required
      />
    </div>
    <p
      v-if="message"
      class="text-danger text-center mb-3"
      id="response-message"
    >
      {{ message }}
    </p>
    <div class="text-center">
      <button type="submit" class="btn btn-primary">Register</button>
    </div>
  </form>
  <p class="text-center pt-3">
    Already have an account?
    <RouterLink to="/influencer/login" class="text-decoration-none">Sign In</RouterLink>
  </p>
</div>
`,
  data() {
    return {
      formData: {
        username: '',
        email: '',
        password: '',
        inf_category: '',
        inf_niche: '',
        inf_reach: '',
      },
      message: ''
    };
  },
  methods: {
    async registerInfluencer() {
      try {
        const response = await axios.post('/server/register?role=influencer', {
          username: this.formData.username,
          email: this.formData.email,
          password: this.formData.password,
          inf_category: this.formData.inf_category,
          inf_niche: this.formData.inf_niche,
          inf_reach: this.formData.inf_reach
        },{headers: {
      'Content-Type': 'application/x-www-form-urlencoded'},withCredentials: true });
        this.message =
          response.data.message === true
            ? 'Registration successful!'
            : response.data.message;
            const user_data_response = await axios.get('/server/get_user', { withCredentials: true })
        const user = user_data_response.data
        localStorage.setItem('user', JSON.stringify(user))
        this.$router.push('/influencer')
      } catch (error) {
        this.message = 'An error occurred during registration.'+error.response.data.message;
      }
    }
  }
};

/*
<style scoped>
.registration-container {
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

.registration-form {
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

p {
  text-align: center;
  color: #ff0000;
}
</style>
*/