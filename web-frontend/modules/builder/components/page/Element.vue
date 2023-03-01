<template>
  <div>
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
  },
  computed: {
    elementType() {
      return this.$registry.get('element', this.element.type)
    },
  },
}
</script>
