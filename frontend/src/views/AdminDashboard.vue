<template>
  <div>
    <h2>Admin Dashboard</h2>
    <div v-if="pendingUsers.length">
      <h3>Pending Approvals</h3>
      <ul>
        <li v-for="user in pendingUsers" :key="user.id">
          {{ user.email }} ({{ user.role }})
          <button @click="approveUser(user.id)">Approve</button>
        </li>
      </ul>
    </div>
    <div v-else>
      <p>No pending approvals.</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      pendingUsers: [],
    };
  },
  async created() {
    const response = await axios.get('http://localhost:5000/admin/pending_users', { withCredentials: true });
    this.pendingUsers = response.data.users;
  },
  methods: {
    async approveUser(userId) {
      await axios.post(`http://localhost:5000/admin/approve_user/${userId}`, {}, { withCredentials: true });
      this.pendingUsers = this.pendingUsers.filter(user => user.id !== userId);
    },
  },
};
</script>
