<template>
<div id="sponsor-navbar">
    <nav class="navbar navbar-dark navbar-expand-lg bg-primary">
    <div class="container-fluid" style="max-width: 100vw;">
    <RouterLink class="navbar-brand" to="/"><h1 class="h3">IESCP</h1></RouterLink>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation" >
        <span class="navbar-toggler-icon"></span>
    </button>

    <div class="collapse navbar-collapse justify-content-end" id="navbarSupportedContent">
        <div class="navbar-nav mr-auto">
            <RouterLink to="/sponsor" class="nav-item nav-link">Dashboard</RouterLink>
            <RouterLink to="/campaigns" class="nav-item nav-link">Campaigns</RouterLink>
            <RouterLink to="/adrequest" class="nav-link">Ad Request</RouterLink>
            <RouterLink to="/connect" class="nav-link">Connect</RouterLink>
        </div>
        <form class="d-flex">
            <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search"></input>
            <button class="btn btn-success me-4" type="submit">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-search" viewBox="0 0 16 16">
                <path d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001q.044.06.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1 1 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0"/>
                </svg>
            </button>
        </form>
        <a class="nav-link text-white" href="#" @click="logout">Logout</a>
    </div>
    </div>
    </nav>
    </div>
</template>

<script>
import axios from 'axios'
import { RouterLink } from 'vue-router';
export default {
    methods: {
        logout() {
            const response=axios.get('/server/logout', { withCredentials: true })
            if (response.data.message === 'Logged out') {
                localStorage.removeItem('user')
                localStorage.removeItem('userRole')
                this.$router.push('/')
            }
        }
    }
}
</script>