import axios from "axios";
  
  export default {
    template: `
        <div class="container mt-4">
          <h1 class="text-center mb-4">Find Influencers</h1>
      
          <!-- Search Bar -->
          <div class="input-group mb-4">
            <input
              type="text"
              class="form-control"
              v-model="searchQuery"
              placeholder="Search by name, industry, niche, or reach"
            />
            <button class="btn btn-primary" @click="filterInfluencers">Search</button>
          </div>
      
          <!-- Influencers Display -->
          <div class="row">
            <div
              v-for="influencer in filteredInfluencers"
              :key="influencer.inf_id"
              class="col-md-4 mb-4"
            >
              <div class="card h-100">
                <div class="card-body">
                  <h5 class="card-title">{{ influencer.username }}</h5>
                  <p class="card-text">
                    <strong>Industry:</strong> {{ influencer.inf_category }}<br />
                    <strong>Niche:</strong> {{ influencer.inf_niche }}<br />
                    <strong>Reach:</strong> {{ influencer.inf_reach }}
                  </p>
                  <button
                    class="btn btn-primary"
                    @click="openAdRequestModal(influencer.inf_id)"
                  >
                    Request Ad
                  </button>
                </div>
              </div>
            </div>
          </div>
      
          <!-- Ad Request Modal -->
          <div
            v-if="showModal"
            class="modal fade show d-block"
            tabindex="-1"
            role="dialog"
            style="background-color: rgba(0, 0, 0, 0.5)"
          >
            <div class="modal-dialog" role="document">
              <div class="modal-content">
                <div class="modal-header">
                  <h5 class="modal-title">Request Ad</h5>
                  <button type="button" class="btn-close" @click="closeModal"></button>
                </div>
                <div class="modal-body">
                  <label for="campaign">Select Campaign:</label>
                  <select
                    class="form-select mb-3"
                    v-model="selectedCampaign"
                    required
                  >
                    <option
                      v-for="campaign in campaigns"
                      :key="campaign.cmpn_id"
                      :value="campaign.cmpn_id"
                    >
                      {{ campaign.cmpn_name }}
                    </option>
                  </select>
                  <textarea
                    v-model="adMessage"
                    class="form-control mb-3"
                    placeholder="Enter ad message"
                    required
                  ></textarea>
                  <input
                    type="number"
                    v-model="paymentAmt"
                    class="form-control mb-3"
                    placeholder="Enter payment amount"
                    required
                  />
                </div>
                <div class="modal-footer">
                  <button class="btn btn-primary" @click="requestAd">Submit</button>
                  <button class="btn btn-secondary" @click="closeModal">Cancel</button>
                </div>
              </div>
            </div>
          </div>
        </div>`,
    data() {
      return {
        searchQuery: "",
        influencers: [],
        filteredInfluencers: [],
        campaigns: [],
        showModal: false,
        selectedCampaign: null,
        adMessage: "",
        paymentAmt: null,
        selectedInfluencer: null,
      };
    },
    created() {
      this.fetchInfluencers();
    },
    methods: {
      async fetchInfluencers() {
        try {
          const response = await axios.get("/api/influencers");
          this.influencers = response.data;
          this.filteredInfluencers = this.influencers; // Default view shows all influencers
        } catch (error) {
          console.error("Error fetching influencers:", error);
        }
      },
      filterInfluencers() {
        const query = this.searchQuery.toLowerCase();
        this.filteredInfluencers = this.influencers.filter(
          (influencer) =>
            influencer.username.toLowerCase().includes(query) ||
            influencer.inf_category.toLowerCase().includes(query) ||
            influencer.inf_niche.toLowerCase().includes(query) ||
            influencer.inf_reach.toString().includes(query)
        );
      },
      async fetchCampaigns() {
        try {
          const response = await axios.get("/api/campaigns");
          this.campaigns = response.data;
        } catch (error) {
          console.error("Error fetching campaigns:", error);
        }
      },
      openAdRequestModal(infId) {
        this.selectedInfluencer = infId;
        this.fetchCampaigns();
        this.showModal = true;
      },
      async requestAd() {
        try {
          await axios.post("/api/ad-requests", {
            cmpn_id: this.selectedCampaign,
            inf_id: this.selectedInfluencer,
            message: this.adMessage,
            payment_amt: this.paymentAmt,
          });
          alert("Ad request submitted successfully!");
          this.closeModal();
        } catch (error) {
          console.error("Error submitting ad request:", error);
          alert("Failed to submit ad request.");
        }
      },
      closeModal() {
        this.showModal = false;
        this.selectedCampaign = null;
        this.adMessage = "";
        this.paymentAmt = null;
      },
    },
  };