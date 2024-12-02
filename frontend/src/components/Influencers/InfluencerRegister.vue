<template>
  <div class="registration-container">
    <h1>Register as an Influencer</h1>
    <form @submit.prevent="registerInfluencer">
      <div class="registration-form">
        <label for="username">Username:</label>
        <input
          type="text"
          id="username"
          v-model="formData.username"
          required
        />
      </div>
      <div class="registration-form">
        <label for="email">Email:</label>
        <input
          type="email"
          id="email"
          v-model="formData.email"
          required
        />
      </div>
      <div class="registration-form">
        <label for="password">Password:</label>
        <input
          type="password"
          id="password"
          v-model="formData.password"
          required
        />
      </div>
      <div class="registration-form">
        <label for="inf_category">Category:</label>
        <input
          type="text"
          id="inf_category"
          v-model="formData.inf_category"
          required
        />
      </div>
      <div class="registration-form">
        <label for="inf_niche">Niche:</label>
        <input
          type="text"
          id="inf_niche"
          v-model="formData.inf_niche"
          required
        />
      </div>
      <div class="registration-form">
        <label for="inf_reach">Reach:</label>
        <input
          type="number"
          id="inf_reach"
          v-model="formData.inf_reach"
          required
        />
      </div>
      <p v-if="message" class="text-danger text-center" id="response-message">{{ message }}</p>
      <button type="submit">Register</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
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
</script>

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
