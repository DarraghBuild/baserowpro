import { ApplicationType } from '@baserow/modules/core/applicationTypes'
import BuilderForm from '@baserow/modules/builder/components/form/BuilderForm'
import SidebarComponentBuilder from '@baserow/modules/builder/components/sidebar/SidebarComponentBuilder'
import { populatePage } from '@baserow/modules/builder/store/page'

export class BuilderApplicationType extends ApplicationType {
  static getType() {
    return 'builder'
  }

  getIconClass() {
    return 'iconoir-apple-imac-2021'
  }

  getName() {
    const { i18n } = this.app
    return i18n.t('applicationType.builder')
  }

  getDefaultName() {
    const { i18n } = this.app
    return i18n.t('applicationType.builderDefaultName')
  }

  getApplicationFormComponent() {
    return BuilderForm
  }

  getSidebarComponent() {
    return SidebarComponentBuilder
  }

  populate(application) {
    const values = super.populate(application)
    values.pages.forEach((object, pages) => populatePage(object))
    return values
  }

  delete(application, { $router }) {
    const pageSelected = application.pages.some((page) => page._.selected)
    if (pageSelected) {
      $router.push({ name: 'dashboard' })
    }
  }

  select(application, { $router, $i18n, $store }, callback = null) {
    const pages = application.pages
      .map((p) => p)
      .sort((a, b) => a.order - b.order)

    if (pages.length > 0) {
      $router.push(
        {
          name: 'builder-page',
          params: {
            builderId: application.id,
            pageId: pages[0].id,
          },
        },
        callback
      )
      return true
    } else {
      $store.dispatch('toast/error', {
        title: $i18n.t('applicationType.cantSelectPageTitle'),
        message: $i18n.t('applicationType.cantSelectPageDescription'),
      })
      return false
    }
  }
}
