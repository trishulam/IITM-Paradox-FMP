import Vue from 'vue'
import VueRouter from 'vue-router'
import HomeView from '../views/HomeView.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'login',
    component: () => import(/* webpackChunkName: "about" */ '../views/LoginView.vue')
  },
  {
    path: '/dashboard',
    // name: 'home',
    component: HomeView,
    props: true,
    children: [
      {
        path: '/',
        name: 'pending-bills',
        props: true,
        component: () => import(/* webpackChunkName: "about" */ '../views/PendingBillsView.vue')
      },
      {
        path: '/verified-bills',
        name: 'verified-bills',
        props: true,
        component: () => import(/* webpackChunkName: "about" */ '../views/VerifiedBillsView.vue')
      },
      {
        path: '/all-pending-bills',
        name: 'all-pending-bills',
        props: true,
        component: () => import(/* webpackChunkName: "about" */ '../views/AllPendingBillsView.vue')
      },
      {
        path: 'approved-bills',
        name: 'approved-bills',
        props: true,
        component: () => import(/* webpackChunkName: "about" */ '../views/ApprovedBillsView.vue')
      },
      {
        path: '/processed-bills',
        name: 'processed-bills',
        props: true,
        component: () => import(/* webpackChunkName: "about" */ '../views/ProcessedBillsView.vue')
      },
      {
        path: '/generate-eas',
        name: 'generate-eas',
        props: true,
        component: () => import(/* webpackChunkName: "about" */ '../views/GenerateEasView.vue')
      },
      {
        path: '/view-eas',
        name: 'view-eas',
        props: true,
        component: () => import(/* webpackChunkName: "about" */ '../views/ViewEasView.vue')
      },
      {
        path: '/voucher',
        name: 'voucher',
        props: true,
        component: () => import(/* webpackChunkName: "about" */ '../views/VoucherView.vue')
      },
      {
        path: 'pod-dashboard',
        name: 'pod-dashboard',
        props: true,
        component: () => import(/* webpackChunkName: "about" */ '../views/PodDashboardView.vue')
      }
    ]
  },
  {
    path: '/bill-form',
    name: 'bill-form',
    component: () => import('../views/BillFormView.vue')
  },
  {
    path: '/bill-success',
    name: 'bill-success',
    component: () => import('../views/BillSuccessView.vue')
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
