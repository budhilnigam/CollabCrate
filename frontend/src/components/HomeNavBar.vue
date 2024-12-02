<script>
import { RouterLink } from "vue-router"
</script>
<template>
<div id="home-navbar">
    <nav class="navbar navbar-dark navbar-expand-lg bg-primary">
    <div class="container-fluid" style="max-width: 100vw;">
    <RouterLink class="navbar-brand" to="/">Logo Here</RouterLink>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation" >
        <span class="navbar-toggler-icon"></span>
    </button>

    <div class="collapse navbar-collapse justify-content-end" id="navbarSupportedContent">
        <div class="navbar-nav mr-auto">
            <RouterLink to="/" class="nav-item nav-link">Home</RouterLink>
            <RouterLink to="/About" class="nav-item nav-link">About</RouterLink>
            <RouterLink to="/sponsor" class="nav-link">Sponsors</RouterLink>
            <RouterLink to="/influencer" class="nav-link">Influencers</RouterLink>
        </div>
        <form class="d-flex">
            <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search"></input>
            <button class="btn btn-outline-success" type="submit">Search</button>
        </form>
        </div>
    </div>
    </nav>
    </div>
</template>

export default {
    components: {
        RouterLink
    }
}