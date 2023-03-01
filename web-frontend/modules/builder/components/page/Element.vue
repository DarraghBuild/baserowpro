<template>
  <div
    class="element"
    :class="{ 'element--active': active }"
    @click="$emit('selected')"
  >
    <component :is="elementType.component"></component>
  </div>
</template>

<script>
export default {
  name: 'Element',
  props: {
    element: {
      type: Object,
      required: true,
    },
    active: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
  computed: {
    elementType() {
      return this.$registry.get('element', this.element.type)
    },
  },
}
</script>
