
  import axios from 'axios';
  import SponsorCampaignForm from '@/components/Sponsors/SponsorCampaignForm';
  import EditCampaignForm from '@/components/Sponsors/EditCampaignForm';
  import NegotiationBox from '@/components/NegotiationBox';
  export default {
    template: `
    <div class="px-2 m-2">
      <h1>Sponsor Dashboard</h1>
      <div class="row text-center mb-4">
      <div class="col-md-3 mb-3">
        <div class="card shadow-sm">
          <div class="card-body">
            <h5 class="card-title">Active Campaigns</h5>
            <p class="card-text display-6">{{ stats.active_campaigns }}</p>
          </div>
        </div>
      </div>
      <div class="col-md-3 mb-3">
        <div class="card shadow-sm">
          <div class="card-body">
            <h5 class="card-title">Completed Campaigns</h5>
            <p class="card-text display-6">{{ stats.completed_campaigns }}</p>
          </div>
        </div>
      </div>
      <div class="col-md-3 mb-3">
        <div class="card shadow-sm">
          <div class="card-body">
            <h5 class="card-title">Pending Requests</h5>
            <p class="card-text display-6">{{ stats.pending_requests }}</p>
          </div>
        </div>
      </div>
      <div class="col-md-3 mb-3">
        <div class="card shadow-sm">
          <div class="card-body">
            <h5 class="card-title">Completed Requests</h5>
            <p class="card-text display-6">{{ stats.completed_requests }}</p>
          </div>
        </div>
      </div>
    </div>
    <h2 class="mb-3">Campaigns</h2>
    <div class="table-responsive mb-4">
      <table class="table table-bordered">
        <thead class="table-dark">
          <tr>
            <th>Campaign Name</th>
            <th>Description</th>
            <th>Start Date</th>
            <th>End Date</th>
            <th>Budget</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="campaign in stats.campaigns" :key="campaign.cmpn_id">
            <td>{{ campaign.cmpn_name }}</td>
            <td>{{ campaign.cmpn_description }}</td>
            <td>{{ campaign.start_date }}</td>
            <td>{{ campaign.end_date }}</td>
            <td>{{ campaign.budget }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <h2 class="mb-3">Ad Requests</h2>
    <div class="table-responsive">
      <table class="table table-bordered">
        <thead class="table-dark">
          <tr>
            <th>Campaign</th>
            <th>Influencer</th>
            <th>Message</th>
            <th>Payment Amount</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="request in stats.ad_requests" :key="request.ad_id">
            <td>{{ request.cmpn_name }}</td>
            <td>{{ request.username }}</td>
            <td>{{ request.message }}</td>
            <td>{{ request.payment_amt }}</td>
            <td>
              <div v-if="request.made_by === 'influencer' && (request.status === 'pending' || request.status === 'negotiated')">
                <button @click="handleAdRequestAction(request.ad_id, 'accepted', 'Ad accepted')" class="btn btn-success">Accept</button>
                <button @click="handleAdRequestAction(request.ad_id, 'rejected', 'Ad rejected')" class="btn btn-danger">Reject</button>
                <NegotiationBox :adId="request.ad_id"></NegotiationBox>
              </div>
              <div v-else>
                {{ request.status[0].toUpperCase()+request.status.slice(1).toLowerCase() }}
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
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
                <li><strong>Budget:</strong> \${{ campaign.budget }}</li>
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
    </div>`,
    data() {
      return {
        campaigns: [],
        stats:null,
      };
    },
    async created() {
      this.fetchCampaigns();
      fetch('/server/user/info')
      .then((response) => response.json())
      .then((data) => {
        this.stats = data;
      })
      .catch((error) => console.error('Error fetching sponsor data:', error));
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
      fetchUserInfo(){
        fetch('/server/user/info')
      .then((response) => response.json())
      .then((data) => {
        this.stats = data;
      })
      .catch((error) => console.error('Error fetching influencer data:', error));
      },
      handleAdRequestAction(ad_id, status, message) {
        if (status === 'negotiated') {
          message =prompt("Enter your message");
        }
        fetch('/server/ad_requests/action?ad_id=' + ad_id + '&status=' + status+ '&message=' + message, {
          method: 'PUT',
        })
          .then(response => response.json())
          .then(data => {
            console.log(data.message);
            this.fetchUserInfo();
          })
          .catch(error => console.error('Error:', error));
      },
    },
    components: {
      'CampaignForm': SponsorCampaignForm,
      'EditCampaignForm': EditCampaignForm,
      'NegotiationBox':NegotiationBox
    },
  };
