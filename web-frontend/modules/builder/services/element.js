export default (client) => {
  return {
    create(pageId, elementType) {
      return client.post(`builder/page/${pageId}/elements/`, {
        type: elementType,
      })
    },
  }
}
