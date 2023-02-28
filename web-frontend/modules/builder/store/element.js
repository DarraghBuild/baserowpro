import ElementService from '@baserow/modules/builder/services/element'

const state = {
  elements: [],
}

const mutations = {
  ADD_ITEM(state, element) {
    state.elements.push(element)
  },
}

const actions = {
  forceCreate({ commit }, element) {
    commit('ADD_ITEM', element)
  },
  async create({ dispatch }, { page, elementType }) {
    const { data: element } = await ElementService(this.$client).create(
      page.id,
      elementType.getType()
    )

    dispatch('forceCreate', element)
  },
  async fetch({ dispatch }, { page }) {
    const { data: elements } = await ElementService(this.$client).fetchAll(
      page.id
    )

    elements.forEach((element) => dispatch('forceCreate', element))

    return elements
  },
}

const getters = {}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
}
