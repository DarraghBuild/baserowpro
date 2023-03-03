<template>
  <div
    class="element"
    :class="{ 'element--active': active }"
    @click="$emit('selected')"
  >
    <InsertElementButton
      v-if="active"
      class="element__insert--top"
      @click="$emit('insert', 'top')"
    />
    <ElementMenu
      v-if="active"
      :move-up-disabled="isFirstElement"
      :move-down-disabled="isLastElement"
      @delete="$emit('delete')"
      @move="$emit('move', $event)"
    />
    <component
      :is="elementType.component"
      class="element__component"
    ></component>
    <InsertElementButton
      v-if="active"
      class="element__insert--bottom"
      @click="$emit('insert', 'bottom')"
    />
  </div>
</template>

<script>
import ElementMenu from '@baserow/modules/builder/components/page/ElementMenu'
import InsertElementButton from '@baserow/modules/builder/components/page/InsertElementButton'
export default {
  name: 'Element',
  components: { ElementMenu, InsertElementButton },
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
    isLastElement: {
      type: Boolean,
      required: false,
      default: false,
    },
    isFirstElement: {
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
