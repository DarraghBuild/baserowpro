import { Registerable } from '@baserow/modules/core/registry'
import ParagraphElement from '@baserow/modules/builder/components/elements/components/ParagraphElement'
import HeadingElement from '@baserow/modules/builder/components/elements/components/HeadingElement'
import LinkElement from '@baserow/modules/builder/components/elements/components/LinkElement'
import ParagraphElementForm from '@baserow/modules/builder/components/elements/components/forms/general/ParagraphElementForm'
import HeadingElementForm from '@baserow/modules/builder/components/elements/components/forms/general/HeadingElementForm'
import LinkElementForm from '@baserow/modules/builder/components/elements/components/forms/general/LinkElementForm'
import ImageElementForm from '@baserow/modules/builder/components/elements/components/forms/general/ImageElementForm'
import ImageElement from '@baserow/modules/builder/components/elements/components/ImageElement'
import InputTextElement from '@baserow/modules/builder/components/elements/components/InputTextElement.vue'
import InputTextElementForm from '@baserow/modules/builder/components/elements/components/forms/general/InputTextElementForm.vue'
import TableElement from '@baserow/modules/builder/components/elements/components/TableElement.vue'
import TableElementForm from '@baserow/modules/builder/components/elements/components/forms/general/TableElementForm.vue'

import {
  ELEMENT_EVENTS,
  PAGE_PARAM_TYPE_VALIDATION_FUNCTIONS,
} from '@baserow/modules/builder/enums'
import ColumnElement from '@baserow/modules/builder/components/elements/components/ColumnElement'
import ColumnElementForm from '@baserow/modules/builder/components/elements/components/forms/general/ColumnElementForm'
import _ from 'lodash'
import DefaultStyleForm from '@baserow/modules/builder/components/elements/components/forms/style/DefaultStyleForm'
import { compile } from 'path-to-regexp'
import ButtonElement from '@baserow/modules/builder/components/elements/components/ButtonElement'
import ButtonElementForm from '@baserow/modules/builder/components/elements/components/forms/general/ButtonElementForm'
import { ClickEvent } from '@baserow/modules/builder/eventTypes'

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

  get editComponent() {
    return this.component
  }

  get generalFormComponent() {
    return null
  }

  get styleFormComponent() {
    return DefaultStyleForm
  }

  get stylesAll() {
    return ['style_padding_top', 'style_padding_bottom']
  }

  get styles() {
    return this.stylesAll
  }

  get events() {
    return []
  }

  getEvents() {
    return this.events.map((EventType) => new EventType(this.app))
  }

  /**
   * Returns whether the element configuration is valid or not.
   * @param {object} param An object containing the element and the builder
   * @returns true if the element is in error
   */
  isInError({ element, builder }) {
    return false
  }

  /**
   * This hook allows you to change the values given by the form of the element before
   * they are sent to the backend to update the element.
   *
   * @param {object} values - The values of the element
   * @returns {*}
   */
  prepareValuesForRequest(values) {
    return values
  }

  onElementEvent(event, params) {}
}

export class ContainerElementType extends ElementType {
  get elementTypesAll() {
    return Object.values(this.app.$registry.getAll('element'))
  }

  /**
   * Returns an array of element types that are not allowed as children of this element.
   *
   * @returns {Array}
   */
  get childElementTypesForbidden() {
    return []
  }

  get childElementTypes() {
    return _.difference(this.elementTypesAll, this.childElementTypesForbidden)
  }

  /**
   * Returns an array of style types that are not allowed as children of this element.
   * @returns {Array}
   */
  get childStylesForbidden() {
    return []
  }

  get defaultPlaceInContainer() {
    throw new Error('Not implemented')
  }
}

export class ColumnElementType extends ContainerElementType {
  getType() {
    return 'column'
  }

  get name() {
    return this.app.i18n.t('elementType.column')
  }

  get description() {
    return this.app.i18n.t('elementType.columnDescription')
  }

  get iconClass() {
    return 'iconoir-view-columns-3'
  }

  get component() {
    return ColumnElement
  }

  get generalFormComponent() {
    return ColumnElementForm
  }

  get childElementTypesForbidden() {
    return this.elementTypesAll.filter(
      (elementType) => elementType instanceof ContainerElementType
    )
  }

  get defaultPlaceInContainer() {
    return '0'
  }
}

export class HeadingElementType extends ElementType {
  static getType() {
    return 'heading'
  }

  get name() {
    return this.app.i18n.t('elementType.heading')
  }

  get description() {
    return this.app.i18n.t('elementType.headingDescription')
  }

  get iconClass() {
    return 'iconoir-text'
  }

  get component() {
    return HeadingElement
  }

  get generalFormComponent() {
    return HeadingElementForm
  }
}

export class ParagraphElementType extends ElementType {
  static getType() {
    return 'paragraph'
  }

  get name() {
    return this.app.i18n.t('elementType.paragraph')
  }

  get description() {
    return this.app.i18n.t('elementType.paragraphDescription')
  }

  get iconClass() {
    return 'iconoir-text-box'
  }

  get component() {
    return ParagraphElement
  }

  get generalFormComponent() {
    return ParagraphElementForm
  }
}

export class LinkElementType extends ElementType {
  static getType() {
    return 'link'
  }

  get name() {
    return this.app.i18n.t('elementType.link')
  }

  get description() {
    return this.app.i18n.t('elementType.linkDescription')
  }

  get iconClass() {
    return 'iconoir-link'
  }

  get component() {
    return LinkElement
  }

  get generalFormComponent() {
    return LinkElementForm
  }

  isInError({ element, builder }) {
    return LinkElementType.arePathParametersInError(element, builder)
  }

  static arePathParametersInError(element, builder) {
    if (
      element.navigation_type === 'page' &&
      !isNaN(element.navigate_to_page_id)
    ) {
      const destinationPage = builder.pages.find(
        ({ id }) => id === element.navigate_to_page_id
      )

      if (destinationPage) {
        const destinationPageParams = destinationPage.path_params || []
        const pageParams = element.page_parameters || []

        const destinationPageParamNames = destinationPageParams.map(
          ({ name }) => name
        )
        const pageParamNames = pageParams.map(({ name }) => name)

        if (!_.isEqual(destinationPageParamNames, pageParamNames)) {
          return true
        }
      }
    } //

    return false
  }

  static getUrlFromElement(element, builder, resolveFormula) {
    if (element.navigation_type === 'page') {
      if (!isNaN(element.navigate_to_page_id)) {
        const page = builder.pages.find(
          ({ id }) => id === element.navigate_to_page_id
        )

        // The builder page list might be empty or the page has been deleted
        if (!page) {
          return ''
        }

        const paramTypeMap = Object.fromEntries(
          page.path_params.map(({ name, type }) => [name, type])
        )

        const toPath = compile(page.path, { encode: encodeURIComponent })
        const pageParams = Object.fromEntries(
          element.page_parameters.map(({ name, value }) => [
            name,
            PAGE_PARAM_TYPE_VALIDATION_FUNCTIONS[paramTypeMap[name]](
              resolveFormula(value)
            ),
          ])
        )
        return toPath(pageParams)
      }
    } else {
      return resolveFormula(element.navigate_to_url)
    }
    return ''
  }
}

export class ImageElementType extends ElementType {
  getType() {
    return 'image'
  }

  get name() {
    return this.app.i18n.t('elementType.image')
  }

  get description() {
    return this.app.i18n.t('elementType.imageDescription')
  }

  get iconClass() {
    return 'iconoir-media-image'
  }

  get component() {
    return ImageElement
  }

  get generalFormComponent() {
    return ImageElementForm
  }
}

export class InputTextElementType extends ElementType {
  getType() {
    return 'input_text'
  }

  get name() {
    return this.app.i18n.t('elementType.inputText')
  }

  get description() {
    return this.app.i18n.t('elementType.inputTextDescription')
  }

  get iconClass() {
    return 'iconoir-input-field'
  }

  get component() {
    return InputTextElement
  }

  get generalFormComponent() {
    return InputTextElementForm
  }
}

export class ButtonElementType extends ElementType {
  getType() {
    return 'button'
  }

  get name() {
    return this.app.i18n.t('elementType.button')
  }

  get description() {
    return this.app.i18n.t('elementType.buttonDescription')
  }

  get iconClass() {
    return 'iconoir-square-cursor'
  }

  get component() {
    return ButtonElement
  }

  get generalFormComponent() {
    return ButtonElementForm
  }

  get events() {
    return [ClickEvent]
  }
}

export class TableElementType extends ElementType {
  getType() {
    return 'table'
  }

  get name() {
    return this.app.i18n.t('elementType.table')
  }

  get description() {
    return this.app.i18n.t('elementType.tableDescription')
  }

  get iconClass() {
    return 'iconoir-table'
  }

  get component() {
    return TableElement
  }

  get generalFormComponent() {
    return TableElementForm
  }

  prepareValuesForRequest(values) {
    const prepared = { ...values }

    if (!prepared?.fields?.length || prepared.fields.length === 0) {
      prepared.fields = [
        {
          name: `${this.app.i18n.t('tableElementForm.fieldDefaultName')} 1`,
          value: '',
        },
        {
          name: `${this.app.i18n.t('tableElementForm.fieldDefaultName')} 2`,
          value: '',
        },
        {
          name: `${this.app.i18n.t('tableElementForm.fieldDefaultName')} 3`,
          value: '',
        },
      ]
    }

    return prepared
  }

  onElementEvent(event, { page, element, dataSourceId }) {
    if (event === ELEMENT_EVENTS.DATA_SOURCE_REMOVED) {
      if (element.data_source_id === dataSourceId) {
        // Remove the data_source_id
        this.app.store.dispatch('element/forceUpdate', {
          page,
          element,
          values: { data_source_id: null },
        })
      }
    }
  }
}
