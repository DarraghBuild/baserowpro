import DataSourceService from '@baserow/modules/builder/services/dataSource'

const state = {}

const mutations = {
  SET_CONTENT(state, { element, value, range }) {
    const [offset] = range
    const missingIndexes = offset + value.length - element._.content.length

    let newContent

    if (missingIndexes > 0) {
      newContent = element._.content.concat(Array(missingIndexes).fill(null))
    } else {
      newContent = [...element._.content]
    }

    value.forEach((record, index) => {
      newContent[offset + index] = record
    })

    element._.content = newContent
  },
  SET_HAS_MORE_PAGE(state, { element, value }) {
    element._.hasNextPage = value
  },

  CLEAR_CONTENT(state, { element }) {
    element._.content = []
    element._.hasNextPage = false
  },
  SET_LOADING(state, { element, value }) {
    element._.contentLoading = value
  },
}

const actions = {
  /**
   * Fetch the data from the server and add them to the element store.
   * @param {object} dataSource the data source we want to dispatch
   * @param {object} data the query body
   */
  async fetchElementContent(
    { commit, getters },
    { element, dataSource, range, data: dispatchContext, replace = false }
  ) {
    if (!dataSource.type) {
      return
    }

    const serviceType = this.app.$registry.get('service', dataSource.type)

    commit('SET_LOADING', { element, value: true })
    const previousContent = [...getters.getElementContent(element)]
    try {
      if (serviceType.isValid(dataSource)) {
        const {
          data: { results, has_next_page: hasNextPage },
        } = await DataSourceService(this.app.$client).dispatch(
          dataSource.id,
          dispatchContext,
          { range }
        )
        if (replace) {
          commit('CLEAR_CONTENT', {
            element,
          })
        }
        commit('SET_CONTENT', {
          element,
          value: results,
          range,
        })
        commit('SET_HAS_MORE_PAGE', {
          element,
          value: hasNextPage,
        })
      } else {
        commit('CLEAR_CONTENT', {
          element,
        })
      }
    } catch (e) {
      commit('SET_CONTENT', { element, value: previousContent, range })
      throw e
    }
    commit('SET_LOADING', { element, value: false })
  },

  clearElementContent({ commit }, { element }) {
    commit('CLEAR_CONTENT', { element })
  },
}

const getters = {
  getElementContent: (state) => (element) => {
    return element._.content
  },
  getHasMorePage: (state) => (element) => {
    return element._.hasNextPage
  },
  getLoading: (state) => (element) => {
    return element._.contentLoading
  },
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
}
