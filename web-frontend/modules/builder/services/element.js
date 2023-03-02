export default (client) => {
  return {
    fetchAll(pageId) {
      return client.get(`builder/page/${pageId}/elements/`)
    },
    create(pageId, elementType) {
      return client.post(`builder/page/${pageId}/elements/`, {
        type: elementType,
      })
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
