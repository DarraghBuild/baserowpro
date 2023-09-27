import WorkflowActionService from '@baserow/modules/builder/services/workflowAction'

const state = {}

const mutations = {
  ADD_ITEM(state, { page, workflowAction }) {
    page.workflowActions.push(workflowAction)
  },
  SET_ITEMS(state, { page, workflowActions }) {
    page.workflowActions = workflowActions
  },
  DELETE_ITEM(state, { page, workflowActionId }) {
    const index = page.workflowActions.findIndex(
      (workflowAction) => workflowAction.id === workflowActionId
    )
    if (index > -1) {
      page.workflowActions.splice(index, 1)
    }
  },
}

const actions = {
  forceCreate({ commit }, { page, workflowAction }) {
    commit('ADD_ITEM', { page, workflowAction })
  },
  forceDelete({ commit }, { page, workflowActionId }) {
    commit('DELETE_ITEM', { page, workflowActionId })
  },
  async create(
    { dispatch },
    { page, workflowActionType, eventType, configuration = null }
  ) {
    const { data: workflowAction } = await WorkflowActionService(
      this.$client
    ).create(page.id, workflowActionType, eventType, configuration)

    await dispatch('forceCreate', { page, workflowAction })

    return workflowAction
  },
  async fetch({ commit }, { page }) {
    const { data: workflowActions } = await WorkflowActionService(
      this.$client
    ).fetchAll(page.id)

    commit('SET_ITEMS', { page, workflowActions })
  },
  async delete({ dispatch }, { page, workflowAction }) {
    dispatch('forceDelete', { page, workflowActionId: workflowAction.id })

    try {
      await WorkflowActionService(this.$client).delete(workflowAction.id)
    } catch (error) {
      await dispatch('forceCreate', { page, workflowAction })
      throw error
    }
  },
}

const getters = {
  getElementWorkflowActions: (state) => (page, elementId) => {
    return page.workflowActions.filter(
      (workflowAction) => workflowAction.element_id === elementId
    )
  },
}

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters,
}
