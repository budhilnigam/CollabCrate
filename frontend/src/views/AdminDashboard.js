import axios from "axios";
export default {
  template: `
  <div class="container mt-5">
    <div class="row mb-4">
      <div class="col-md-3" v-for="(value, key) in stats" :key="key">
        <div class="card text-center">
          <div class="card-body">
            <h5 class="card-title">{{ key }}</h5>
            <p class="card-text">{{ value }}</p>
          </div>
        </div>
      </div>
    </div>

    <ul class="nav nav-tabs mb-4">
      <li class="nav-item">
        <a class="nav-link" :class="{ active: activeTab === 'users' }" href="#" @click="activeTab = 'users'">Users</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" :class="{ active: activeTab === 'campaigns' }" href="#" @click="activeTab = 'campaigns'">Campaigns</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" :class="{ active: activeTab === 'adRequests' }" href="#" @click="activeTab = 'adRequests'">Ad Requests</a>
      </li>
    </ul>

    <div v-if="activeTab === 'users'">
      <h4>Users</h4>
      <div key="influencer">
        <h5 class="mt-3 text-capitalize">Influencers</h5>
        <table class="table table-bordered">
          <thead>
            <tr>
              <th>ID</th>
              <th>Username</th>
              <th>Email</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in users.influencers" :key="user.inf_id">
              <td>{{ user.inf_id }}</td>
              <td>{{ user.username }}</td>
              <td>{{ user.email }}</td>
              <td>{{ user.flagged ? 'Flagged' : 'Active' }}</td>
              <td>
                <button class="btn btn-sm" :class="user.flagged ? 'btn-danger' : 'btn-success'" @click="toggleFlag('users', 'influencer', user)">
                  {{ user.flagged ? 'Unflag' : 'Flag' }}
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div key="sponsor">
        <h5 class="mt-3 text-capitalize"> Sponsors </h5>
        <table class="table table-bordered">
          <thead>
            <tr>
              <th>ID</th>
              <th>Username</th>
              <th>Email</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in users.sponsors" :key="user.sp_id">
              <td>{{ user.sp_id }}</td>
              <td>{{ user.username }}</td>
              <td>{{ user.email }}</td>
              <td>{{ user.flagged ? 'Flagged' : 'Active' }}</td>
              <td>
                <button class="btn btn-sm" :class="user.flagged ? 'btn-danger' : 'btn-success'" @click="toggleFlag('users', 'sponsor', user)">
                  {{ user.flagged ? 'Unflag' : 'Flag' }}
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <div v-else-if="activeTab === 'campaigns'">
      <h4>Campaigns</h4>
      <table class="table table-bordered">
        <thead>
          <tr>
            <th>ID</th>
            <th>Title</th>
            <th>Description</th>
            <th>Goals</th>
            <th>Visibility</th>
            <th>Budget</th>
            <th>Sponsor</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="campaign in campaigns" :key="campaign.cmpn_id">
            <td>{{ campaign.cmpn_id }}</td>
            <td>{{ campaign.cmpn_name }}</td>
            <td>{{ campaign.cmpn_description }}</td>
            <td>{{ campaign.goals }}</td>
            <td class="btn btn-sm text-white" :class="campaign.visibility=='public' ? 'bg-success' : 'bg-danger'">{{ campaign.visibility[0].toUpperCase()+campaign.visibility.slice(1).toLowerCase() }}</td>
            <td>{{ campaign.budget }}</td>
            <td>{{ campaign.sp_username }}</td>
            <td>{{ campaign.flagged ? 'Flagged' : 'Active' }}</td>
            <td>
              <button class="btn btn-sm" :class="campaign.flagged ? 'btn-danger' : 'btn-success'" @click="toggleFlag('campaigns', null, campaign)">
                {{ campaign.flagged ? 'Unflag' : 'Flag' }}
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-else-if="activeTab === 'adRequests'">
      <h4>Ad Requests</h4>
      <table class="table table-bordered">
        <thead>
          <tr>
            <th>ID</th>
            <th>Message</th>
            <th>Payment Amount</th>
            <th>Made By</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="request in adRequests" :key="request.ad_id">
            <td>{{ request.ad_id }}</td>
            <td>{{ request.message }}</td>
            <td>{{ request.payment_amt }}</td>
            <td>{{ request.made_by }}</td>
            <td>{{ request.status }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>`,
  data() {
    return {
      stats: {},
      activeTab: "campaigns",
      users: {},
      campaigns: [],
      adRequests: []
    };
  },
  created() {
    this.fetchData();
  },
  methods: {
    async fetchData() {
      try {
        const [usersResponse, campaignsResponse, adRequestsResponse] = await Promise.all([
          axios.get("/server/admin/users"),
          axios.get("/server/admin/campaigns"),
          axios.get("/server/admin/ad_requests")
        ]);

        this.users = usersResponse.data;
        this.campaigns = campaignsResponse.data;
        this.adRequests = adRequestsResponse.data;

        this.stats = {
          "Total Influencers": this.users.influencers.length,
          "Total Sponsors": this.users.sponsors.length,
          "Total Campaigns": this.campaigns.length,
          "Active Campaigns": this.campaigns.filter(c => !c.flagged).length
        };
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    },
    async toggleFlag(type, userType, item) {
      try {
        const flagEndpoint = type === "users" ? `/server/users/flag` : `/server/campaigns/flag`;
        let params = {};
        if (type=="users"){
          if (userType === 'influencer') {
            params = { user_type: 'influencer', user_id: item.inf_id , flag: item.flagged ? 0 : 1};
          } else if (userType === 'sponsor') {
            params = { user_type: 'sponsor', user_id: item.sp_id, flag: item.flagged ? 0 : 1 };
          }
        } else {
          params = { cmpn_id: item.cmpn_id , flag: item.flagged ? 0 : 1}
        }
        await axios.put(flagEndpoint, null, { params });

        item.flagged = !item.flagged;
      } catch (error) {
        console.error("Error toggling flag:", error);
      }
    }
  }
};