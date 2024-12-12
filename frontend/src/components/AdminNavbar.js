import axios from 'axios'
import { RouterLink } from 'vue-router';
export default {
    template: `
<div id="admin-navbar">
    <nav class="navbar navbar-dark navbar-expand-lg bg-primary">
    <div class="container-fluid" style="max-width: 100vw;">
    <RouterLink class="navbar-brand" to="/"><h1 class="h3">IESCP</h1></RouterLink>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation" >
        <span class="navbar-toggler-icon"></span>
    </button>

    <div class="collapse navbar-collapse justify-content-end" id="navbarSupportedContent">
        <a class="nav-link text-white" href="#" @click="logout">Logout</a>
    </div>
    </div>
    </nav>
    </div>`,
    methods: {
        async logout() {
            try {
              const response = await axios.get('/server/logout', { withCredentials: true });
              console.log(response);
              // Clear local storage
              localStorage.removeItem('user');
              localStorage.removeItem('userRole');
              // Redirect to home route
              this.$router.push('/');
            } catch (error) {
              console.error('Error during logout:', error);
              alert('Failed to logout. Please try again.');
            }
          }
          
    }
}