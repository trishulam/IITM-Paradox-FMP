import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    billId: localStorage.getItem('billId') || null
  },
  getters: {
    billId(state) {
      return state.billId
    }
  },
  mutations: {
    setBillId(state, billId) {
      state.billId = billId
      localStorage.setItem('billId', billId)
    }
  },
  actions: {
    setBillId({ commit }, billId) {
      commit('setBillId', billId)
    }
  },
  modules: {
  }
})
