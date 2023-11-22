<template>
  <button
    class="button-icon"
    :class="classes"
    :disabled="disabled"
    v-on="$listeners"
  >
    <i v-if="!loading" class="button-icon__icon" :class="icon" />
  </button>
</template>

<script>
export default {
  props: {
    /**
     * The size of the button.
     */
    icon: {
      required: true,
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
     * If true the button will be disabled.
     */
    active: {
      required: false,
      type: Boolean,
      default: false,
    },
  },
  computed: {
    classes() {
      const classObj = {
        'button-icon--loading': this.loading,
        disabled: this.disabled,
        active: this.active,
      }
      return classObj
    },
  },
}
</script>
