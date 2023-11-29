<template>
  <b-container
    style="height: 100vh; display: flex; justify-content: center; align-items: center; flex-direction: column;">
    <b-card title="Finance Paradox 2023" style="width: 30rem; margin: auto;">
      <b-form style="width: 70%; margin: 0 auto" @submit="onSubmit" @reset="onReset">
        <div class="text-left" role="group">
          <label for="input-email">Email:</label>
          <b-form-input id="input-email" v-model="email" required :state="emailState"
            aria-describedby="input-live-help input-live-feedback" placeholder="Enter your email" trim></b-form-input>

          <!-- This will only be shown if the preceding input has an invalid state -->
          <b-form-invalid-feedback id="input-live-feedback">
            Enter a valid email address
          </b-form-invalid-feedback>

          <label class="mt-3" for="input-password">Password:</label>
          <b-form-input id="input-password" type="password" required v-model="password"
            aria-describedby="input-live-help input-live-feedback" placeholder="Enter your password" trim></b-form-input>
        </div>

        <b-button v-if="!isLoggingIn" class="mt-3" type="submit" variant="primary">
          Login
        </b-button>
        <b-button v-if="isLoggingIn" class="mt-3" disabled variant="primary">
          <b-spinner small type="grow"></b-spinner>
          Loggin In...
        </b-button>
        <div>
          <p class="mt-3">For submitting a bill <a :href="bill_form_url">visit here</a></p>
        </div>
      </b-form>
    </b-card>
  </b-container>
</template>

<script>
import axios from 'axios'
import config from '@/config'
export default {
  data() {
    return {
      email: '',
      password: '',
      emailState: null,
      isLoggingIn: false,
      bill_form_url: config.BILL_FORM_URL,
      error: ''
    }
  },
  methods: {
    validateEmail(email) {
      const re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
      return re.test(email)

    },
    onSubmit(event) {
      event.preventDefault()
      this.isLoggingIn = true;

      var formData = new FormData();
      formData.append('email', this.email);
      formData.append('password', this.password);

      axios.post(`${config.API_BASE_URL}/login`, formData)
        .then((response) => {
          if (response.data.success) {
            localStorage.setItem('token', response.data.token);
            if (response.data.admin) {
              this.$router.push('/dashboard/approved-bills');
            } else if(response.data.pod_admin) {
              this.$router.push('/dashboard/pod-dashboard');
            }
            else {
              this.$router.push('/dashboard');
            }
          } else if(!response.data.success) {
            this.error = response.data.error;
            this.$bvToast.toast(this.error, {
              title: 'Error',
              variant: 'danger',
              solid: true
            })
            this.isLoggingIn = false;
          }
        })
        .catch((error) => {
          console.log(error);
        });
    },
    onReset(event) {
      event.preventDefault()
      // Reset our form values
      this.email = ''
      this.username = ''
    },
  },
  watch: {
    email(val) {
      if (val.length < 1) {
        this.emailState = null
        return
      }
      if (this.validateEmail(val)) {
        this.emailState = true
      } else {
        this.emailState = false
      }
    }
  }
}
</script>