<template>
  <div
    class="element"
    :class="{ 'element--active': active }"
    @click="$emit('selected')"
  >
    <ElementMenu v-if="active" @delete="$emit('delete')" />
    <component
      :is="elementType.component"
      class="element__component"
    ></component>
  </div>
</template>

<script>
import ElementMenu from '@baserow/modules/builder/components/page/ElementMenu'
export default {
  name: 'Element',
  components: { ElementMenu },
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
