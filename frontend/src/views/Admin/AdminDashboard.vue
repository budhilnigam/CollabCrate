<template>
    <div class="container my-5">
      <h1 class="text-center mb-4">Admin Dashboard</h1>
      
      <!-- Statistics Section -->
      <div class="row text-center mb-5">
        <div class="col-md-3">
          <div class="card bg-primary text-white">
            <div class="card-body">
              <h4>Total Campaigns</h4>
              <p class="display-6">{{ statistics.totalCampaigns }}</p>
            </div>
          </div>
        </div>
        <div class="col-md-3">
          <div class="card bg-success text-white">
            <div class="card-body">
              <h4>Total Users</h4>
              <p class="display-6">{{ statistics.totalUsers }}</p>
            </div>
          </div>
        </div>
        <div class="col-md-3">
          <div class="card bg-warning text-dark">
            <div class="card-body">
              <h4>Flagged Campaigns</h4>
              <p class="display-6">{{ statistics.flaggedCampaigns }}</p>
            </div>
          </div>
        </div>
        <div class="col-md-3">
          <div class="card bg-danger text-white">
            <div class="card-body">
              <h4>Flagged Users</h4>
              <p class="display-6">{{ statistics.flaggedUsers }}</p>
            </div>
          </div>
        </div>
      </div>
  
      <!-- Campaigns Section -->
      <div class="mb-5">
        <h2 class="mb-3">Campaigns</h2>
        <table class="table table-striped table-bordered">
          <thead class="table-dark">
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Description</th>
              <th>Status</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="campaign in campaigns" :key="campaign.cmpn_id">
              <td>{{ campaign.cmpn_id }}</td>
              <td>{{ campaign.cmpn_name }}</td>
              <td>{{ campaign.cmpn_description }}</td>
              <td>
                <span
                  class="badge"
                  :class="campaign.flagged ? 'bg-danger' : 'bg-success'"
                >
                  {{ campaign.flagged ? "Flagged" : "Active" }}
                </span>
              </td>
              <td>
                <button
                  class="btn btn-warning btn-sm"
                  @click="flagCampaign(campaign.cmpn_id)"
                  :disabled="campaign.flagged"
                >
                  Flag
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
  
      <!-- Users Section -->
      <div>
        <h2 class="mb-3">Users</h2>
        <table class="table table-striped table-bordered">
          <thead class="table-dark">
            <tr>
              <th>ID</th>
              <th>Username</th>
              <th>Type</th>
              <th>Status</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in users" :key="user.id">
              <td>{{ user.id }}</td>
              <td>{{ user.username }}</td>
              <td>{{ user.type }}</td>
              <td>
                <span
                  class="badge"
                  :class="user.flagged ? 'bg-danger' : 'bg-success'"
                >
                  {{ user.flagged ? "Flagged" : "Active" }}
                </span>
              </td>
              <td>
                <button
                  class="btn btn-warning btn-sm"
                  @click="flagUser(user.id)"
                  :disabled="user.flagged"
                >
                  Flag
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  
  export default {
    data() {
      return {
        statistics: {
          totalCampaigns: 0,
          totalUsers: 0,
          flaggedCampaigns: 0,
          flaggedUsers: 0,
        },
        campaigns: [],
        users: [],
      };
    },
    methods: {
      fetchStatistics() {
        axios.get("/api/admin/statistics").then((response) => {
          this.statistics = response.data;
        });
      },
      fetchCampaigns() {
        axios.get("/api/admin/campaigns").then((response) => {
          this.campaigns = response.data;
        });
      },
      fetchUsers() {
        axios.get("/api/admin/users").then((response) => {
          this.users = response.data;
        });
      },
      flagCampaign(campaignId) {
        axios.post(`/api/admin/flag/campaign/${campaignId}`).then(() => {
          this.fetchCampaigns();
        });
      },
      flagUser(userId) {
        axios.post(`/api/admin/flag/user/${userId}`).then(() => {
          this.fetchUsers();
        });
      },
    },
    mounted() {
      this.fetchStatistics();
      this.fetchCampaigns();
      this.fetchUsers();
    },
  };
  </script>
  
  <style>
  .table th, .table td {
    vertical-align: middle;
  }
  </style>  