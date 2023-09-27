export default (client) => {
  return {
    create(pageId, workflowActionType, eventType, configuration = null) {
      const payload = {
        type: workflowActionType,
        event: eventType,
        ...configuration,
      }

      return client.post(`builder/page/${pageId}/workflow_actions/`, payload)
    },
  }
}
