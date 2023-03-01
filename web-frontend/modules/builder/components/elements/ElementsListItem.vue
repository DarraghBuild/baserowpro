<template>
  <a>
    <i :class="`fas fa-${elementType.iconClass}`"></i>
    <span class="margin-left-1"> {{ elementType.name }}</span>
  </a>
</template>

<script>
export default {
  name: 'ElementsListItem',
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
