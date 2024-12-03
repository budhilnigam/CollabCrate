<template>
  <div>
    <h2>Influencer Dashboard</h2>
    <div v-if="adRequests.length">
      <h3>Your Ad Requests</h3>
      <ul>
        <li v-for="request in adRequests" :key="request.ad_id">
          Campaign: {{ request.cmpn_description }} - Status: {{ request.status }}
          <button v-if="request.status === 'Accepted'" @click="respondToRequest(request.id, 'completed')">Complete</button>
          <button v-if="request.status === 'Pending'" @click="respondToRequest(request.id, 'accepted')">Accept</button>
          <button v-if="request.status === 'Pending'" @click="respondToRequest(request.id, 'rejected')">Reject</button>
        </li>
      </ul>
    </div>
    <div v-else>
      <p>No ad requests found.</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data () {
    return {
      adRequests: []
    }
  },
  async created () {
    this.fetchAdRequests()
  },
  methods: {
    async fetchAdRequests () {
      try {
        const response = await axios.get('/server/ad_requests?status=all',{
          headers: {'Content-Type': 'application/json'},
          withCredentials: true })
        this.adRequests = response.data.ads
        console.log(response)
      } catch (error) {
        alert('Failed to fetch ad requests: ' + error.response.data.message)
      }
    },
    async respondToRequest (requestId, status) {
      try {
        await axios.post(`/server/influencer/ad_request/${requestId}/respond`, { status }, { withCredentials: true })
        alert(`Ad request ${status}.`)
        this.fetchAdRequests()
      } catch (error) {
        alert(`Failed to ${status} ad request: ` + error.response.data.message)
      }
    }
  }
}
</script>

<style scoped>
ul {
  list-style-type: none;
  padding: 0;
}
li {
  padding: 10px;
  margin-bottom: 10px;
  border: 1px solid #ccc;
}
</style>
