<template>
    <button
        class="btn btn-primary w-100"
        @click="openAdRequestModal"
    >
        Ad Request
    </button>
<div class="modal fade" id="adRequestModal" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Ad Request</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <form @submit.prevent="submitAdRequest">
          <div class="modal-body">
            <div class="mb-3">
              <label for="message" class="form-label">Message</label>
              <textarea
                id="message"
                v-model="adRequestData.message"
                class="form-control"
                placeholder="Enter your message"
                required
              ></textarea>
            </div>
            <div class="mb-3">
              <label for="paymentAmt" class="form-label">Payment Amount</label>
              <input
                type="number"
                id="paymentAmt"
                v-model="adRequestData.payment_amt"
                class="form-control"
                placeholder="Enter payment amount"
                required
              />
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
            <button type="submit" class="btn btn-primary">Submit Request</button>
          </div>
        </form>
      </div>
    </div>
</div>
</template>

<script>
import axios from 'axios';

export default {
    props: {
        cmpnId: Number,
    },
    data() {
        return {
            adRequestData: {
                cmpn_id: "",
                inf_id: localStorage.getItem("userRole") === "influencer" ? JSON.parse(localStorage.getItem("user")).inf_id : null,
                message: "",
                payment_amt: "",
            },
        }
    },
    methods: {
        openAdRequestModal() {
            this.adRequestData.cmpn_id = this.cmpnId;
            this.adRequestData.message = "";
            this.adRequestData.payment_amt = "";
            const modal = new bootstrap.Modal(document.getElementById("adRequestModal"));
            modal.show();
            },
        async submitAdRequest() {
            try {
                const response = await axios.post(
                `/server/ad_requests?cmpn_id=${this.adRequestData.cmpn_id}&inf_id=${this.adRequestData.inf_id}`,
                {
                    message: this.adRequestData.message,
                    payment_amt: this.adRequestData.payment_amt,
                },
                {
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded'
                    },
                    withCredentials: true,
                }
                );

            if (response.data.message) {
                alert("Ad request submitted successfully!");
                this.fetchCampaigns(); // Refresh the campaigns list
                const modal = bootstrap.Modal.getInstance(
                    document.getElementById("adRequestModal")
                );
                modal.hide();
                }
            } catch (error) {
                console.error("Error submitting ad request:", error);
                alert("Failed to submit ad request. Please try again.");
            }
        },
    }
}
</script>