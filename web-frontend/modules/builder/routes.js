import path from 'path'

export const routes = [
  {
    name: 'builder-page',
    path: '/builder/:builderId/page/:pageId',
    component: path.resolve(__dirname, 'pages/page.vue'),
    props(route) {
      const p = { ...route.params }
      p.builderId = parseInt(p.builderId)
      p.pageId = parseInt(p.pageId)
      return p
    },
  },
]