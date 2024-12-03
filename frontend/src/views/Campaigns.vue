<template>
  <div class="container py-4">
    <h1 class="mb-4">Campaigns</h1>

    <!-- Filters Section -->
    <div class="row mb-4">
      <div class="col-md-4">
        <input
          type="text"
          v-model="filters.name"
          class="form-control"
          placeholder="Search by campaign name"
        />
      </div>
      <div class="col-md-4">
        <input
          type="text"
          v-model="filters.sponsor"
          class="form-control"
          placeholder="Search by sponsor username"
        />
      </div>
      <div class="col-md-4 d-flex align-items-start">
        <button class="btn btn-primary me-2" @click="applyFilters">Apply</button>
        <button class="btn btn-secondary" @click="resetFilters">Reset</button>
      </div>
    </div>

    <!-- Campaign List -->
    <div class="row">
      <div
        v-for="campaign in filteredCampaigns"
        :key="campaign.cmpn_id"
        class="col-md-6 col-lg-4 mb-4"
      >
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">{{ campaign.cmpn_name }}</h5>
            <h6 class="card-subtitle mb-2 text-muted">Sponsor: {{ campaign.sp_username }}</h6>
            <p class="card-text">{{ campaign.cmpn_description }}</p>
            <ul class="list-unstyled">
              <li><strong>Start Date:</strong> {{ campaign.start_date }}</li>
              <li><strong>End Date:</strong> {{ campaign.end_date }}</li>
              <li><strong>Budget:</strong> ${{ campaign.budget }}</li>
              <li><strong>Goals:</strong> {{ campaign.goals }}</li>
            </ul>
            <button v-if="isInfluencer && campaign.ad_id" class="btn btn-warning w-100" disabled>
                {{campaign.status}}
            </button>
            <AdRequestBox
            v-else-if="isInfluencer && !campaign.ad_id"
            cmpnId="campaign.cmpn_id"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import AdRequestBox from "@/components/AdRequestBox.vue";
export default {
  components: {
    'AdRequestBox': AdRequestBox,
  },
  data() {
    return {
      campaigns: [],
      filters: {
        name: "",
        sponsor: "",
      },
      adRequestData: {
        cmpn_id: null,
        message: "",
        payment_amt: "",
      },
      isInfluencer: localStorage.getItem("userRole")==='influencer' ? true : false,
      selectedCampaignId: null,
      showAdRequestModal: false,
    };
  },
  computed: {
    filteredCampaigns() {
      return this.campaigns.filter((campaign) => {
        const matchesName = campaign.cmpn_name
          .toLowerCase()
          .includes(this.filters.name.toLowerCase());
        const matchesSponsor = campaign.sp_username
          .toLowerCase()
          .includes(this.filters.sponsor.toLowerCase());
        return matchesName && matchesSponsor;
      });
    },
  },
  methods: {
    async fetchCampaigns() {
      try {
        const response = await axios.get("/server/campaigns/all");
        this.campaigns = response.data.map((campaign) => ({
          ...campaign,
          hasRequestedAd: campaign.ad_id !== null,
        }));
        console.log("Fetched campaigns:", response.data);
      } catch (error) {
        console.error("Error fetching campaigns:", error);
      }
    },
    openAdRequestModal(cmpn_id) {
      this.selectedCampaignId = cmpn_id;
      this.showAdRequestModal = true;
    },
    closeAdRequestModal() {
      this.showAdRequestModal = false;
    },
    applyFilters() {
      // Filters are applied automatically via computed properties
    },
    resetFilters() {
      this.filters.name = "";
      this.filters.sponsor = "";
    },
  },
  created() {
    this.fetchCampaigns();
    // Set `isInfluencer` based on user role logic (e.g., fetched from API or user session)
  },
};
</script>

<style scoped>
.card {
  border: 1px solid #ddd;
  border-radius: 0.25rem;
}
</style>