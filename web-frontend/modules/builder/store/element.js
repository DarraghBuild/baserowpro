import ElementService from '@baserow/modules/builder/services/element'

const state = {
  // Maps page id to elements on that page
  elements: {},
}

const mutations = {
  ADD_ITEM(state, { element, pageId, beforeId = null }) {
    if (Object.keys(state.elements).includes(pageId.toString())) {
      const isElementAlreadyOnPage = state.elements[pageId].some(
        (e) => e.id === element.id
      )
      if (!isElementAlreadyOnPage) {
        if (beforeId === null) {
          state.elements[pageId].push(element)
        } else {
          const insertionIndex = state.elements[pageId].findIndex(
            (e) => e.id === beforeId
          )
          state.elements[pageId].splice(insertionIndex, 0, element)
        }
      }
    } else {
      state.elements = { ...state.elements, [pageId]: [element] }
    }
  },
  DELETE_ITEM(state, { elementId, pageId }) {
    if (Object.keys(state.elements).includes(pageId.toString())) {
      const index = state.elements[pageId].findIndex(
        (element) => element.id === elementId
      )
      state.elements[pageId].splice(index, 1)
    }
  },
  ORDER_ITEMS(state, { newOrder, pageId }) {
    state.elements[pageId] = newOrder.map((id) =>
      state.elements[pageId].find((element) => element.id === id)
    )
  },
}

const actions = {
  forceCreate({ commit }, { element, pageId, beforeId = null }) {
    commit('ADD_ITEM', { element, pageId, beforeId })
  },
  forceDelete({ commit }, { elementId, pageId }) {
    commit('DELETE_ITEM', { elementId, pageId })
  },
  forceMove({ commit }, { newOrder, pageId }) {
    commit('ORDER_ITEMS', { newOrder, pageId })
  },
  async create({ dispatch }, { page, elementType, beforeId = null }) {
    const { data: element } = await ElementService(this.$client).create(
      page.id,
      elementType.getType(),
      beforeId
    )

    dispatch('forceCreate', { element, pageId: page.id, beforeId })
  },
  async delete({ dispatch }, { element }) {
    await ElementService(this.$client).delete(element.id)

    dispatch('forceDelete', { elementId: element.id, pageId: element.page_id })
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
  async move({ state, dispatch }, { elementId, beforeElementId, pageId }) {
    const order = state.elements[pageId].map((element) => element.id)
    const elementIndex = order.findIndex((id) => id === elementId)
    const indexToSwapWith = order.findIndex((id) => id === beforeElementId)

    // The element could be the last or the first one which we need to handle
    if (indexToSwapWith === -1 || indexToSwapWith === order.length) {
      return
    }

    order[elementIndex] = order[indexToSwapWith]
    order[indexToSwapWith] = elementId

    await ElementService(this.$client).order(pageId, order)

    dispatch('forceMove', { newOrder: order, pageId })
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
