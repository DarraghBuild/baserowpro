<template>
  <div v-if="mode === 'editing'">
    <AddElementZone @add-element="showAddElementModal"></AddElementZone>
    <AddElementModal
      ref="addElementModal"
      :page="page"
      :element-types-allowed="elementType.childElementTypes"
    ></AddElementModal>
  </div>
</template>

<script>
import AddElementZone from '@baserow/modules/builder/components/elements/AddElementZone.vue'
import containerElement from '@baserow/modules/builder/mixins/containerElement'
import AddElementModal from '@baserow/modules/builder/components/elements/AddElementModal.vue'

export default {
  name: 'FormElement',
  components: { AddElementModal, AddElementZone },
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
