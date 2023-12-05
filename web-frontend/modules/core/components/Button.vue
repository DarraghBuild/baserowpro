<template>
  <component
    :is="tag === 'a' || href ? 'a' : 'button'"
    class="button"
    :class="classes"
    :disabled="disabled || loading"
    :active="active"
    v-bind.prop="customBind"
    v-on="$listeners"
  >
    <i v-if="icon" class="button__icon" :class="icon" />
    <span class="button__label"><slot></slot></span>
  </component>
</template>

<script>
export default {
  props: {
    /**
     * The HTML tag to use for the button. Available tags are: a, button.
     */
    tag: {
      required: false,
      type: String,
      default: 'button',
      validator: function (value) {
        return ['a', 'button'].includes(value)
      },
    },
    /**
     * The size of the button.
     */
    size: {
      required: false,
      type: String,
      default: '',
    },
    /**
     * The type of the button. Available types are: primary, secondary, danger.
     */
    type: {
      required: false,
      type: String,
      default: 'primary',
      validator: function (value) {
        return ['primary', 'secondary', 'danger'].includes(value)
      },
    },
    /**
     * The icon of the button.
     */
    icon: {
      required: false,
      type: String,
      default: '',
    },
    /**
     * Wether the button is loading or not.
     */
    loading: {
      required: false,
      type: Boolean,
      default: false,
    },
    /**
     * Wether the button is active or not.
     */
    disabled: {
      required: false,
      type: Boolean,
      default: false,
    },
    /**
     * Make the button full width.
     */
    fullWidth: {
      required: false,
      type: Boolean,
      default: false,
    },
    /**
     * If the button is a link, this is the href.
     */
    href: {
      required: false,
      type: String,
      default: null,
    },
    /**
     * If the button is a link, this is the rel. Available values are: nofollow, noopener, noreferrer.
     */
    rel: {
      required: false,
      type: String,
      default: null,
      validator: function (value) {
        return ['nofollow', 'noopener', 'noreferrer'].includes(value)
      },
    },
    /**
     * If the button is a link, this is the target. Available values are: _blank, _self, _parent, _top.
     */
    target: {
      required: false,
      type: String,
      default: null,
      validator: function (value) {
        return ['_blank', '_self', '_parent', '_top'].includes(value)
      },
    },
  },
  computed: {
    classes() {
      const hasIcon = this.prependIcon || this.appendIcon || this.icon
      const classObj = {
        [`button--${this.size}`]: this.size,
        [`button--${this.type}`]: this.type,
        'button--primary': !this.type,
        'button--full-width': this.fullWidth,
        'button--icon-only': hasIcon && !this.$slots.default,
        'button--loading': this.loading,
        active: this.active && !this.loading && !this.disabled,
        'button--overflow': this.overflow,
      }
      return classObj
    },
    customBind() {
      const attr = {}
      if (this.tag === 'a') {
        attr.href = this.href
        attr.target = this.target
        attr.rel = this.target
      }

      return Object.keys(attr).forEach((key) => {
        if (attr[key] === null) {
          delete attr[key]
        }
      })
    },
  },
}
</script>
