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
  async create({ commit }, { page, elementType }) {
    const { data: element } = await ElementService(this.$client).create(
      page.id,
      elementType.getType()
    )

    commit('ADD_ITEM', element)
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
