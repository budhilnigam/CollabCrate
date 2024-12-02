<template>
    <div class="px-2">
      <h1>Sponsor Dashboard</h1>
      <div>
      </div>
      <div v-if="campaigns.length">
        <span class="d-flex justify-content-between">
          <h3>Your Campaigns</h3>
          <CampaignForm @create-campaign="createCampaign">
          </CampaignForm>
        </span>
        <div v-for="campaign in campaigns" :key="campaign.cmpn_id" class="campaign">
          <h1>{{campaign.cmpn_name}} </h1>
          <h4>{{ campaign.cmpn_description }}</h4>
          <h4><i style="font-weight:bold">Goals: </i>{{ campaign.goals }}</h4>
          <h4><b style="font-weight:bold">Budget: </b>{{ campaign.budget }}</h4>
          <h4> <b>Start Date:</b> {{ Intl.DateTimeFormat('en-GB', { weekday: 'long', day: 'numeric',month: 'long', year: 'numeric' }).format(new Date(campaign.start_date)) }}</h4>
          <h4> <b>End Date:</b> {{ Intl.DateTimeFormat('en-GB', { weekday: 'long', day: 'numeric',month: 'long', year: 'numeric' }).format(new Date(campaign.end_date)) }}</h4>
          <ul>
            <li v-for="request in campaign.requests" :key="request.id">
              {{ request.influencer_email }} - {{ request.status }}
              <button v-if="request.status === 'pending'" @click="cancelRequest(request.id)">Cancel Request</button>
            </li>
          </ul>
          <input v-model="selectedInfluencer" placeholder="Influencer Email" />
          <button @click="sendAdRequest(campaign.cmpn_id)">Send Ad Request</button>
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
  export default {
    data() {
      return {
        campaigns: [],
        selectedInfluencer: '',
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
      async sendAdRequest(campaignId) {
        try {
          await axios.post(`/server/sponsor/campaign/${campaignId}/ad_request`, { influencer_email: this.selectedInfluencer }, { withCredentials: true });
          alert('Ad request sent.');
          this.fetchCampaigns();
        } catch (error) {
          alert('Failed to send ad request: ' + error.response.data.message);
        }
      },
      async cancelRequest(requestId) {
        try {
          await axios.post(`http://localhost:5000/sponsor/campaign/ad_request/${requestId}/cancel`, {}, { withCredentials: true });
          alert('Ad request canceled.');
          this.fetchCampaigns();
        } catch (error) {
          alert('Failed to cancel ad request: ' + error.response.data.message);
        }
      },
      longDate(date) {
        return new Date(date).toLocaleString();
      }
    },
    components: {
      'CampaignForm': SponsorCampaignForm,
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
