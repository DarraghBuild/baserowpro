import { Registerable } from '@baserow/modules/core/registry'
import ParagraphElement from '@baserow/modules/builder/components/page/components/ParagraphElement'

export class ElementType extends Registerable {
  get name() {
    return null
  }

  get description() {
    return null
  }

  get iconClass() {
    return null
  }

  get component() {
    return null
  }
}

export class HeaderElementType extends ElementType {
  getType() {
    return 'header'
  }

  get name() {
    return this.app.i18n.t('elementType.header')
  }

  get description() {
    return this.app.i18n.t('elementType.headerDescription')
  }

  get iconClass() {
    return 'heading'
  }

  get component() {
    return ParagraphElement
  }
}

export class ParagraphElementType extends ElementType {
  getType() {
    return 'paragraph'
  }

  get name() {
    return this.app.i18n.t('elementType.paragraph')
  }

  get description() {
    return this.app.i18n.t('elementType.paragraphDescription')
  }

  get iconClass() {
    return 'paragraph'
  }

  get component() {
    return ParagraphElement
  }
}
