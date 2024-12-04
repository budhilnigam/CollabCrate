
  import axios from 'axios';
  export default {
    template: `
      <button
        id="edit-campaign"
        class="btn btn-primary me-2"
        @click="openModal"
      >
        Edit
      </button>
      <div
        class="modal fade"
        id="campaignModal"
        tabindex="-1"
        role="dialog"
        aria-labelledby="campaignModalLabel"
        aria-hidden="true"
        ref="campaignModal"
      >
        <div class="modal-dialog" role="document">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title" id="campaignModalLabel">Edit Campaign</h5>
              <button
                type="button"
                class="close"
                data-bs-dismiss="modal"
                aria-label="Close"
                @click="closeModal"
              >
                <span aria-hidden="true">&times;</span>
              </button>
            </div>
            <div class="modal-body">
              <form @submit.prevent="editCampaign">
                <div class="form-group">
                  <label for="cmpn_name">Campaign Name</label>
                  <input
                    type="text"
                    class="form-control"
                    id="cmpn_name"
                    v-model="formData.cmpn_name"
                    required
                  />
                </div>
                <div class="form-group">
                  <label for="cmpn_description">Description</label>
                  <textarea
                    class="form-control"
                    id="cmpn_description"
                    v-model="formData.cmpn_description"
                    required
                  ></textarea>
                </div>
                <div class="form-group">
                  <label for="budget">Budget</label>
                  <input
                    type="number"
                    class="form-control"
                    id="budget"
                    v-model="formData.budget"
                    required
                  />
                </div>
                <div class="form-group">
                  <label for="visibility">Visibility</label>
                  <div class="form-check form-switch mt-2">
                    <input
                      class="form-check-input"
                      type="checkbox"
                      id="visibilitySwitch"
                      role="switch"
                      v-model="isPublic"
                      @change="toggleVisibility"
                    />
                    <label
                      class="form-check-label"
                      :class="['badge', isPublic ? 'bg-success' : 'bg-danger']"
                      for="visibilitySwitch"
                    >
                      {{ isPublic? 'Public' : 'Private' }}
                    </label>
                  </div>
                </div>
                <div class="form-group">
                  <label for="start_date">Start Date</label>
                  <input
                    type="date"
                    class="form-control"
                    id="start_date"
                    v-model="formData.start_date"
                    required
                  />
                </div>
                <div class="form-group">
                  <label for="end_date">End Date</label>
                  <input
                    type="date"
                    class="form-control"
                    id="end_date"
                    v-model="formData.end_date"
                    required
                  />
                </div>
                <div class="form-group">
                  <label for="goals">Goals</label>
                  <textarea
                    class="form-control"
                    id="goals"
                    v-model="formData.goals"
                    required
                  ></textarea>
                </div>
                <p :class="['text-center',message.toLowerCase().includes('error','fail') ? 'text-danger' : 'text-success']">{{ message }}</p>
                <div class="modal-footer">
                  <button type="button" class="btn btn-secondary" @click="closeModal">
                    Cancel
                  </button>
                  <button type="submit" class="btn btn-primary">
                    Confirm
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>`,
    props: {
        campaign: {
            type: Object,
            required: true,
        },
    },
    mounted() {
      this.formData.cmpn_name = this.campaign.cmpn_name;
      this.formData.cmpn_description = this.campaign.cmpn_description;
      this.formData.budget = this.campaign.budget;
      this.formData.visibility = this.campaign.visibility;
      this.formData.start_date = this.campaign.start_date;
      this.formData.end_date = this.campaign.end_date;
      this.formData.goals = this.campaign.goals;
      this.isPublic = this.campaign.visibility === 'public';
    },
    data() {
      return {
        isPublic: false,
        formData: {
          cmpn_name: '',
          cmpn_description: '',
          budget: '',
          visibility: '',
          start_date: '',
          end_date: '',
          goals: '',
        },
        message: '',
      };
    },
    methods: {
      openModal() {
        const modal = new bootstrap.Modal(this.$refs.campaignModal);
        modal.show();
      },
      closeModal() {
        const modal = new bootstrap.Modal(this.$refs.campaignModal);
        modal.hide();
        this.resetForm();
      },
      resetForm() {
        this.formData.cmpn_name = this.campaign.cmpn_name;
        this.formData.cmpn_description = this.campaign.cmpn_description;
        this.formData.budget = this.campaign.budget;
        this.formData.visibility = this.campaign.visibility;
        this.formData.start_date = this.campaign.start_date;
        this.formData.end_date = this.campaign.end_date;
        this.formData.goals = this.campaign.goals;
      },
      toggleVisibility() {
        this.formData.visibility = this.isPublic ? 'public' : 'private';
      },
      async editCampaign() {
        try {
          const response = await axios.put('/server/campaigns/edit?cmpn_id=' + this.campaign.cmpn_id,
          {
            cmpn_name: this.formData.cmpn_name,
            cmpn_description: this.formData.cmpn_description,
            budget: this.formData.budget,
            visibility: this.formData.visibility,
            start_date: this.formData.start_date,
            end_date: this.formData.end_date,
            goals: this.formData.goals,
          },
          {
            headers: {
              'Content-Type': 'application/x-www-form-urlencoded',
            },
            withCredentials: true,
          });
          console.log(response);
          const result = await response.data;
          if (response.status < 300) {
            this.message = 'Campaign edited successfully!';
            const t=setTimeout(() => {
              this.closeModal();
            }, 1000);
          } else {
            this.message = result.message || 'An error occurred.';
          }
        } catch (error) {
          this.message = 'An error occurred while creating the campaign.';
        }
      },
    },
  };