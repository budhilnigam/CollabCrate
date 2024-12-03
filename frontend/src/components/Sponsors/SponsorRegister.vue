<template>
  <div class="registration-container">
    <h1>Register as a Sponsor</h1>
    <form @submit.prevent="registerSponsor">
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
        <label for="sp_industry">Industry:</label>
        <input
          type="text"
          id="sp_industry"
          v-model="formData.sp_industry"
          required
        />
      </div>
      <div class="registration-form">
        <label for="sp_budget">Budget:</label>
        <input
          type="number"
          id="sp_budget"
          v-model="formData.sp_budget"
          required
        />
      </div>
      <p v-if="message" class="danger" id="warning-message">{{ message }}</p>
      <button type="submit">Register</button>
    </form>
    <p class="text-center pt-2">Already have an account? <RouterLink to="/sponsor/login">Sign In</RouterLink></p>
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
</style>
