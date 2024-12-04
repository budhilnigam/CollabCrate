import axios from 'axios';

export default {
  template: `
    <button
      class="btn btn-warning text-white"
      @click="openNegRequestModal"
    >
      Negotiate
    </button>
    <div class="modal fade" id="negotiationRequestModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Negotiate Ad Request</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <form @submit.prevent="submitNegRequest">
            <div class="modal-body">
              <div class="mb-3">
                <label for="message" class="form-label">Message</label>
                <textarea
                  id="message"
                  v-model="negRequestData.message"
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
                  v-model="negRequestData.payment_amt"
                  class="form-control"
                  placeholder="Enter payment amount"
                  required
                />
              </div>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
              <button type="submit" class="btn btn-primary">Submit</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  `,
  props: {
    adId: {
      type: Number,
      required: true,
    },
  },
  data() {
    return {
      negRequestData: {
        message: '',
        payment_amt: '',
      },
    };
  },
  methods: {
    openNegRequestModal() {
      this.negRequestData.message = '';
      this.negRequestData.payment_amt = '';
      const modal = new bootstrap.Modal(document.getElementById('negotiationRequestModal'));
      modal.show();
    },
    submitNegRequest() {
      const { message, payment_amt } = this.negRequestData;
      if (!message || !payment_amt) {
        alert('Both message and payment amount are required!');
        return;
      }
      const status = 'negotiated';
      this.handleNegRequestAction(this.adId, status, message);
    },
    handleNegRequestAction(ad_id, status, message) {
      fetch(`/server/ad_requests/action?ad_id=${ad_id}&status=${status}&message=${encodeURIComponent(message)}&payment_amt=${this.negRequestData.payment_amt}`, {
        method: 'PUT',
      })
        .then((response) => response.json())
        .then((data) => {
          console.log(data.message);
          this.$emit('refreshUserInfo'); // Notify parent to refresh user info
          const modal = bootstrap.Modal.getInstance(document.getElementById('negotiationRequestModal'));
          modal.hide();
        })
        .catch((error) => {
          console.error('Error:', error);
          alert('Failed to process the ad request. Please try again.');
        });
    },
  },
};