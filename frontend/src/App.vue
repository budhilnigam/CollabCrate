<script setup>
import { RouterLink, RouterView } from 'vue-router'
import HomeNavBar from './components/HomeNavBar.js';
import SponsorNavBar from './components/Sponsors/SponsorNavBar.js';
import InfluencerNavBar from './components/Influencers/InfluencerNavBar.js';
import AdminNavbar from './components/AdminNavbar.js';
let userType='anonymous';
if(localStorage.getItem('userRole')!==null){
    userType=localStorage.getItem('userRole');
}
</script>
<template>
    <div style="width:100%;margin:auto">
    <HomeNavBar v-if="userType==='anonymous'"/>
    <SponsorNavBar v-else-if="userType==='sponsor'"/>
    <InfluencerNavBar v-else-if="userType==='influencer'"/>
    <AdminNavbar v-else-if="userType==='admin'"/>
    </div>
    <RouterView />
</template>