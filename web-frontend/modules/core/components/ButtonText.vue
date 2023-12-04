<template>
  <component
    :is="tag === 'a' || href ? 'a' : 'button'"
    class="button-text"
    :class="classes"
    :disabled="disabled || loading"
    :active="active"
    :rel="rel"
    v-bind.prop="customBind"
    v-on="$listeners"
  >
    <i
      v-if="icon !== '' && !loading"
      class="button-text__icon"
      :class="`iconoir-${icon}`"
    />

    <i v-if="loading" class="button-text__spinner"></i>
    <span><slot /></span>
  </component>
</template>

<script>
export default {
  props: {
    /**
     * The tag to use for the root element.
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
      default: 'regular',
      validator: function (value) {
        return ['regular', 'small'].includes(value)
      },
    },
    /**
     * The type of the button.
     */
    type: {
      required: false,
      type: String,
      default: 'primary',
      validator: function (value) {
        return ['primary', 'secondary'].includes(value)
      },
    },
    /**
     * The icon of the button. Must be a valid iconoir or baserow icon class name.
     */
    icon: {
      required: false,
      type: String,
      default: '',
    },
    /**
     * If true a loading icon will be shown.
     */
    loading: {
      required: false,
      type: Boolean,
      default: false,
    },
    /**
     * If true the button will be disabled.
     */
    disabled: {
      required: false,
      type: Boolean,
      default: false,
    },
    /**
     * If true the button will be active.
     */
    active: {
      required: false,
      type: Boolean,
      default: false,
    },
    /**
     * The href attribute of the button.
     */
    href: {
      required: false,
      type: String,
      default: '',
    },
    /**
     * The rel attribute of the button.
     */
    rel: {
      required: false,
      type: String,
      default: '',
    },
    /**
     * The target attribute of the button.
     */
    target: {
      required: false,
      type: String,
      validator: function (value) {
        return ['_blank', '_self'].includes(value)
      },
      default: '_self',
    },
  },
  computed: {
    classes() {
      const classObj = {
        [`button-text--${this.size}`]: this.size !== 'regular',
        [`button-text--${this.type}`]: this.type !== 'primary',
        'button-text--loading': this.loading,
      }
      return classObj
    },
    customBind() {
      const attr = {}
      if (this.href) attr.href = this.href
      if (this.target) attr.target = `${this.target}`
      return attr
    },
  },
}
</script>
