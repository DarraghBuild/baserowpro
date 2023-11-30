<template>
  <div v-if="mode === 'editing' && children.length === 0">
    <AddElementZone @add-element="showAddElementModal"></AddElementZone>
    <AddElementModal
      ref="addElementModal"
      :page="page"
      :element-types-allowed="elementType.childElementTypes"
    ></AddElementModal>
  </div>
  <div v-else>
    <template v-for="(child, index) in children">
      <ElementPreview
        v-if="mode === 'editing'"
        :key="child.id"
        class="element"
        :element="child"
        :active="child.id === elementSelectedId"
        :index="index"
        :placements="[PLACEMENTS.BEFORE, PLACEMENTS.AFTER]"
        :placements-disabled="getPlacementsDisabledVertical(index)"
        @move="moveVertical(child, index, $event)"
      />
      <PageElement v-else :key="child.id" :element="child" :mode="mode" />
    </template>
  </div>
</template>

<script>
import AddElementZone from '@baserow/modules/builder/components/elements/AddElementZone.vue'
import containerElement from '@baserow/modules/builder/mixins/containerElement'
import AddElementModal from '@baserow/modules/builder/components/elements/AddElementModal.vue'
import ElementPreview from '@baserow/modules/builder/components/elements/ElementPreview.vue'
import PageElement from '@baserow/modules/builder/components/page/PageElement.vue'

export default {
  name: 'FormContainerElement',
  components: { PageElement, ElementPreview, AddElementModal, AddElementZone },
  mixins: [containerElement],
  methods: {
    showAddElementModal() {
      this.$refs.addElementModal.show({
        placeInContainer: null,
        parentElementId: this.element.id,
      })
    },
  },
}
</script>
