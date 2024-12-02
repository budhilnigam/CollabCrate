<script setup>
import { RouterLink, RouterView } from 'vue-router'
import HomeNavBar from './components/HomeNavBar.vue';
import SponsorNavBar from './components/Sponsors/SponsorNavBar.vue';
import InfluencerNavBar from './components/Influencers/InfluencerNavBar.vue';
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
    </div>
    <RouterView />
</template>