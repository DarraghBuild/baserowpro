export default (client) => {
  return {
    fetchAll(pageId) {
      return client.get(`builder/page/${pageId}/elements/`)
    },
    create(pageId, elementType, beforeId = null) {
      const payload = {
        type: elementType,
      }

      if (beforeId !== null) {
        payload.before_id = beforeId
      }

      return client.post(`builder/page/${pageId}/elements/`, payload)
    },
    delete(elementId) {
      client.delete(`builder/element/${elementId}/`)
    },
    order(pageId, newOrder) {
      client.post(`builder/page/${pageId}/elements/order/`, {
        element_ids: newOrder,
      })
    },
  }
}
