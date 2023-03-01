import ElementService from '@baserow/modules/builder/services/element'

const state = {
  // Maps page id to elements on that page
  elements: {},
}

const mutations = {
  ADD_ITEM(state, { element, pageId }) {
    if (Object.keys(state.elements).includes(pageId.toString())) {
      state.elements[pageId].push(element)
    } else {
      state.elements[pageId] = [element]
    }
  },
}

const actions = {
  forceCreate({ commit }, { element, pageId }) {
    commit('ADD_ITEM', { element, pageId })
  },
  async create({ dispatch }, { page, elementType }) {
    const { data: element } = await ElementService(this.$client).create(
      page.id,
      elementType.getType()
    )

    dispatch('forceCreate', { element, pageId: page.id })
  },
  async fetch({ dispatch }, { page }) {
    const { data: elements } = await ElementService(this.$client).fetchAll(
      page.id
    )

    elements.forEach((element) =>
      dispatch('forceCreate', { element, pageId: page.id })
    )

    return elements
  },
}

const getters = {
  getElements: (state) => (pageId) => {
    return state.elements[pageId] || []
  },
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
}
