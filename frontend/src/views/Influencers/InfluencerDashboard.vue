<template>
  <div class="container my-4">
    <h1 class="mb-4">Influencer Dashboard</h1>
    <div class="row text-center mb-4">
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
      <div class="col-md-3 mb-3">
        <div class="card shadow-sm">
          <div class="card-body">
            <h5 class="card-title">Ongoing Campaigns</h5>
            <p class="card-text display-6">{{ stats.ongoing_campaigns }}</p>
          </div>
        </div>
      </div>
      <div class="col-md-3 mb-3">
        <div class="card shadow-sm">
          <div class="card-body">
            <h5 class="card-title">Previous Campaigns</h5>
            <p class="card-text display-6">{{ stats.previous_campaigns }}</p>
          </div>
        </div>
      </div>
    </div>
    <h2 class="mb-3">Ad Requests</h2>
    <div class="table-responsive">
      <table class="table table-bordered">
        <thead class="table-dark">
          <tr>
            <th>Campaign</th>
            <th>Start Date</th>
            <th>End Date</th>
            <th>Sponsor</th>
            <th>Status</th>
            <th>Message</th>
            <th>Payment Amount</th>
            <th>Made By</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="request in stats.ad_requests" :key="request.ad_id">
            <td>{{ request.cmpn_name }}</td>
            <td>{{ request.start_date }}</td>
            <td>{{ request.end_date }}</td>
            <td>{{ request.sp_username }}</td>
            <td class="text-center">{{ request.status }}</td>
            <td>{{ request.message }}</td>
            <td>{{ request.payment_amt }}</td>
            <td>
              <div v-if="request.made_by === 'sponsor'">
                  <button @click="handleAdRequestAction(request.ad_id, 'accepted', 'Ad accepted')" class="btn btn-success">Accept</button>
                  <button @click="handleAdRequestAction(request.ad_id, 'rejected', 'Ad rejected')" class="btn btn-danger">Reject</button>
                  <button @click="handleAdRequestAction(request.ad_id, 'negotiated', 'Ad negotiation initiated')" class="btn btn-warning">Negotiate</button>
                </div>
              </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      stats: {},
    };
  },
  created() {
    fetch('/server/user/info')
      .then((response) => response.json())
      .then((data) => {
        this.stats = data;
      })
      .catch((error) => console.error('Error fetching influencer data:', error));
  },
  methods: {
    handleAdRequestAction(ad_id, status, message) {
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
      fetchUserInfo(){
        fetch('/server/user/info')
      .then((response) => response.json())
      .then((data) => {
        this.stats = data;
      })
      .catch((error) => console.error('Error fetching influencer data:', error));
      }
  },
};
</script>