import WorkflowActionService from '@baserow/modules/builder/services/workflowAction'

const state = {}

const mutations = {
  ADD_ITEM(state, { page, workflowAction }) {
    page.workflowActions.push(workflowAction)
  },
}

const actions = {
  forceCreate({ commit }, { page, workflowAction }) {
    commit('ADD_ITEM', { page, workflowAction })
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
