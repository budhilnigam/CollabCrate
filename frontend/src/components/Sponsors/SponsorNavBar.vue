<script>
import { RouterLink } from "vue-router"
</script>
<template>
<div id="sponsor-navbar">
    <nav class="navbar navbar-dark navbar-expand-lg bg-primary">
    <div class="container-fluid" style="max-width: 100vw;">
    <a class="navbar-brand" href="#">Logo Here</a>
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