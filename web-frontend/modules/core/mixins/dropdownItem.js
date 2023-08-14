import { escapeRegExp } from '@baserow/modules/core/utils/string'

export default {
  isDropdownItem: true,

  props: {
    value: {
      validator: () => true,
      required: true,
    },
    name: {
      type: String,
      required: true,
    },
    icon: {
      type: String,
      required: false,
      default: null,
    },
    image: {
      type: String,
      required: false,
      default: null,
    },
    iconTooltip: {
      type: String,
      required: false,
      default: null,
    },
    description: {
      type: String,
      required: false,
      default: null,
    },
    disabled: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
  // data() {
  //   return {
  //     // This field is being used by `getDropdownItemComponents` in ``dropdown.js to
  //     // figure out if the child component is a dropdown item or not
  //     isDropdownItem: true,
  //     query: '',
  //   }
  // },
  methods: {
    select(value, disabled) {
      if (!disabled) {
        this.parent.select(value)
      }
    },
    hover(value, disabled) {
      if (!disabled && this.parent.hover !== value) {
        this.parent.hover = value
      }
    },
    search(parent) {
      return this.isVisible(parent)
    },
    isVisible(parent) {
      const query = parent.query
      if (!query) {
        return true
      }
      const regex = new RegExp('(' + escapeRegExp(query) + ')', 'i')
      return this.name.match(regex)
    },
    isActive(value, parent) {
      return parent.value === value
    },
    isHovering(value, parent) {
      return parent.hover === value
    },
  },
}
