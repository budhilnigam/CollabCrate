<template>
    <div class="px-2 m-2">
      <h1>Sponsor Dashboard</h1>
      <div>
      </div>
      <div v-if="campaigns.length">
        <span class="d-flex justify-content-between">
          <h3>Your Campaigns</h3>
          <CampaignForm>
          </CampaignForm>
        </span>
        <div class="row mt-3">
        <div
          v-for="campaign in campaigns"
          :key="campaign.cmpn_id"
          class="col-md-6 col-lg-4 mb-4"
        >
          <div class="card">
            <div class="card-body">
              <h5 class="card-title">{{ campaign.cmpn_name }}</h5>
              <p class="card-text">{{ campaign.cmpn_description }}</p>
              <ul class="list-unstyled">
                <li><strong>Start Date:</strong> {{ Intl.DateTimeFormat('en-GB', { weekday: 'long', day: 'numeric',month: 'long', year: 'numeric' }).format(new Date(campaign.start_date)) }}</li>
                <li><strong>End Date:</strong> {{ Intl.DateTimeFormat('en-GB', { weekday: 'long', day: 'numeric',month: 'long', year: 'numeric' }).format(new Date(campaign.end_date)) }}</li>
                <li><strong>Budget:</strong> ${{ campaign.budget }}</li>
                <li><strong>Goals:</strong> {{ campaign.goals }}</li>
                <li><strong>Status:</strong><p :class="['d-inline px-1 ms-1 rounded text-white',campaign.visibility === 'public' ? 'bg-success' : 'bg-warning']">{{ campaign.visibility[0].toUpperCase()+campaign.visibility.slice(1).toLowerCase() }}</p></li>
              </ul>
              <div class="mt-3">
                <EditCampaignForm :campaign="campaign"></EditCampaignForm>
                <button class="btn btn-danger" @click="deleteCampaign(campaign.cmpn_id)">Delete</button>
              </div>
            </div>
          </div>
        </div>
      </div>
      </div>
      <div v-else>
        <p>No campaigns found.</p>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import SponsorCampaignForm from '@/components/Sponsors/SponsorCampaignForm.vue';
  import EditCampaignForm from '@/components/Sponsors/EditCampaignForm.vue';
  export default {
    data() {
      return {
        campaigns: [],
      };
    },
    async created() {
      this.fetchCampaigns();
    },
    methods: {
      async createCampaign() {
        try {
          const response = await axios.post('/server/sponsor/campaign', this.newCampaign, { withCredentials: true });
          this.campaigns.push(response.data.campaign);
          this.newCampaign.description = '';
          this.newCampaign.budget = '';
        } catch (error) {
          alert('Failed to create campaign: ' + error.response.data.message);
        }
      },
      async fetchCampaigns() {
        try {
          const response = await axios.get('/server/campaigns/me', { withCredentials: true });
          console.log(response.data)
          this.campaigns = response.data;
          
        } catch (error) {
          alert('Failed to fetch campaigns: ' + error.response.data.message);
        }
      },
    },
    components: {
      'CampaignForm': SponsorCampaignForm,
      'EditCampaignForm': EditCampaignForm,
    },
  };
</script>
  <style scoped>
  .campaign {
    margin-top: 20px;
    padding: 10px;
    border: 1px solid #ccc;
  }
  </style>
