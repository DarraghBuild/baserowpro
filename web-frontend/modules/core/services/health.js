export default (client) => {
  return {
    getAll() {
      return client.get('/_health/full/')
    },
  }
}
