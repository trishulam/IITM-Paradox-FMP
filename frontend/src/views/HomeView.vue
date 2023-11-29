<template>
  <div class="home">
    <div v-if="loading" style="display: flex; justify-content: center; align-items: center; height: 100vh;">
      <b-spinner type="grow" label="Loading..."></b-spinner>
    </div>
    <div v-else-if="!isAuthenticated && !loading">
      <h1>User Not Authenticated</h1>
    </div>
    <div v-else>
      <NavBar :user_data="user_data" />
      <b-container fluid>
        <b-row>
          <b-col class="col-1" cols="2">
            <div>
              <div class="d-flex align-items-center justify-content-start mt-3">
                <b-avatar size="3.5rem"></b-avatar>
                <div class="text-left ml-3">
                  <h4 class="m-0">{{ user_data.name }}</h4>
                  <h6 class="m-0">{{ user_data.role }}</h6>
                </div>
              </div>
              <hr class="solid">
              <b-list-group class="text-dark mt-5">
                <b-list-group-item v-if="user_data.role != 'admin' && user_data.role != 'pod-admin'"
                  class="d-flex justify-content-between align-items-center">
                  <router-link :to="{ name: 'pending-bills' }">
                    Pending Bills
                  </router-link>
                </b-list-group-item>

                <b-list-group-item v-if="user_data.role != 'admin' && user_data.role != 'pod-admin'"
                  class="d-flex justify-content-between align-items-center">
                  <router-link :to="{ name: 'verified-bills' }">
                    Verified Bills
                  </router-link>
                </b-list-group-item>

                <b-list-group-item v-if="user_data.role == 'Core'"
                  class="d-flex justify-content-between align-items-center">
                  <router-link :to="{ name: 'all-pending-bills' }">
                    Show all Pending Bills
                  </router-link>
                </b-list-group-item>

                <b-list-group-item v-if="user_data.role == 'Core'"
                  class="d-flex justify-content-between align-items-center">
                  <router-link :to="{ name: 'generate-eas' }">
                    Generate EAS
                  </router-link>
                </b-list-group-item>

                <b-list-group-item v-if="user_data.role == 'Core'"
                  class="d-flex justify-content-between align-items-center">
                  <router-link :to="{ name: 'view-eas' }">
                    View EAS Generated Bills
                  </router-link>
                </b-list-group-item>
                <!-- for stact admin -->
                <b-list-group-item v-if="user_data.role == 'admin'"
                  class="d-flex justify-content-between align-items-center">
                  <router-link :to="{ name: 'approved-bills' }">
                    Approved Bills
                  </router-link>
                </b-list-group-item>

                <b-list-group-item v-if="user_data.role == 'admin'"
                  class="d-flex justify-content-between align-items-center">
                  <router-link :to="{ name: 'processed-bills' }">
                    Processed Bills
                  </router-link>
                </b-list-group-item>

                <!-- for pod admin -->
                <b-list-group-item v-if="user_data.role == 'pod-admin'"
                  class="d-flex justify-content-between align-items-center">
                  <router-link :to="{ name: 'pod-dashboard' }">
                    Approved Bills
                  </router-link>
                </b-list-group-item>

                <b-list-group-item v-if="user_data.role == 'pod-admin'"
                  class="d-flex justify-content-between align-items-center">
                  <router-link :to="{ name: 'processed-bills' }">
                    Processed Bills
                  </router-link>
                </b-list-group-item>
              </b-list-group>

              <div v-if="user_data.role == 'Super Coordinator'" class="text-left mt-5">
                <h5>Managing Departments</h5>
                <div class="d-flex flex-wrap">
                  <div v-for="(department, index) in user_data.departments" :key="index" class="mr-1">
                    <h5><b-badge variant="secondary" pill>{{ department }}</b-badge></h5>
                  </div>
                </div>
              </div>
            </div>
          </b-col>
          <b-col class="col-2" cols="10">
            <!-- <h1 class="my-4">Pending Bills</h1>
          <BillTable /> -->
            <router-view />
          </b-col>
        </b-row>
      </b-container>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import NavBar from '@/components/NavBar.vue'
import axios from 'axios';
import config from '@/config'
export default {
  name: 'HomeView',
  components: {
    NavBar,
  },
  data() {
    return {
      isAuthenticated: false,
      loading: true,
      user_data: {},
    };
  },
  mounted() {
    if (!localStorage.getItem('token')) {
      setTimeout(() => {
        this.$router.push('/');
      }, 5000);
      this.loading = false;
    } else {
      this.isAuthenticated = true;
      axios.get(`${config.API_BASE_URL}/user`, {
        headers: {
          'x-access-token': localStorage.getItem('token'),
        },
      }).then((res) => {
        this.user_data = res.data;
        this.loading = false;
      }).catch((err) => {
        console.log(err);
      });
    }
  }
}
</script>

<style scoped>
.home {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.col-1 {
  background-color: #2c3e50;
  color: #fff;
  min-height: 100vh;
  padding-top: 60px;
}

.col-2 {
  min-height: 100vh;
  padding-top: 60px;
}

.solid {
  border-top: 1px solid #bbb;
}
</style>
