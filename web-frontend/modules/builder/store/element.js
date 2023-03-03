import ElementService from '@baserow/modules/builder/services/element'

const state = {
  // Maps page id to elementsMap on that page
  elementsMap: {},
}

const mutations = {
  ADD_ITEM(state, { element, pageId, beforeId = null }) {
    if (Object.keys(state.elementsMap).includes(pageId.toString())) {
      const isElementAlreadyOnPage = state.elementsMap[pageId].some(
        (e) => e.id === element.id
      )
      if (!isElementAlreadyOnPage) {
        if (beforeId === null) {
          state.elementsMap[pageId].push(element)
        } else {
          const insertionIndex = state.elementsMap[pageId].findIndex(
            (e) => e.id === beforeId
          )
          state.elementsMap[pageId].splice(insertionIndex, 0, element)
        }
      }
    } else {
      state.elementsMap = { ...state.elementsMap, [pageId]: [element] }
    }
  },
  DELETE_ITEM(state, { elementId, pageId }) {
    if (Object.keys(state.elementsMap).includes(pageId.toString())) {
      const index = state.elementsMap[pageId].findIndex(
        (element) => element.id === elementId
      )
      state.elementsMap[pageId].splice(index, 1)
    }
  },
  ORDER_ITEMS(state, { newOrder, pageId }) {
    state.elementsMap[pageId] = newOrder.map((id) =>
      state.elementsMap[pageId].find((element) => element.id === id)
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
  async create({ dispatch }, { pageId, elementType, beforeId = null }) {
    const { data: element } = await ElementService(this.$client).create(
      pageId,
      elementType,
      beforeId
    )

    dispatch('forceCreate', { element, pageId, beforeId })
  },
  async delete({ dispatch }, { elementId, pageId }) {
    await ElementService(this.$client).delete(elementId)

    dispatch('forceDelete', { elementId, pageId })
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
    const order = state.elementsMap[pageId].map((element) => element.id)
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
  async copy({ state, dispatch }, { elementId, pageId }) {
    const element = state.elementsMap[pageId].find((e) => e.id === elementId)
    await dispatch('create', {
      pageId,
      elementType: element.type,
      beforeId: element.id,
    })
  },
}

const getters = {
  getElements: (state) => (pageId) => {
    return state.elementsMap[pageId] || []
  },
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
}
