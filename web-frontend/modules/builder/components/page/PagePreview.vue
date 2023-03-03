<template>
  <div class="page-preview__wrapper">
    <div
      v-if="deviceType"
      ref="preview"
      class="page-preview"
      :style="{ 'max-width': maxWidth }"
    >
      <div ref="previewScaled" class="page-preview__scaled">
        <Element
          v-for="(element, index) in elements"
          :key="element.id"
          :element="element"
          :active="element.id === elementActiveId"
          :is-first-element="index === 0"
          :is-last-element="index === elements.length - 1"
          @selected="elementActiveId = element.id"
          @delete="deleteElement(element)"
          @move="move(element, index, $event)"
          @insert="insert(element, index, $event)"
        />
      </div>
    </div>
    <AddElementModal ref="addElementModal" :page="page" @add="addElement" />
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import Element from '@baserow/modules/builder/components/page/Element'
import { notifyIf } from '@baserow/modules/core/utils/error'
import AddElementModal from '@baserow/modules/builder/components/elements/AddElementModal'

export default {
  name: 'PagePreview',
  components: { AddElementModal, Element },
  data() {
    return {
      elementActiveId: null,
      // This value is set when the insertion of a new element is in progress to
      // indicate where the element should be inserted
      beforeId: null,
    }
  },
  computed: {
    ...mapGetters({
      page: 'page/getSelected',
      deviceTypeSelected: 'page/getDeviceTypeSelected',
    }),
    elements() {
      return this.$store.getters['element/getElements'](this.page.id)
    },
    deviceType() {
      return this.deviceTypeSelected
        ? this.$registry.get('device', this.deviceTypeSelected)
        : null
    },
    maxWidth() {
      return this.deviceType?.maxWidth
        ? `${this.deviceType.maxWidth}px`
        : 'unset'
    },
  },
  watch: {
    deviceType(value) {
      this.$nextTick(() => {
        this.resized(value)
      })
    },
  },
  methods: {
    ...mapActions({
      actionCreateElement: 'element/create',
      actionMoveElement: 'element/move',
      actionDeleteElement: 'element/delete',
    }),
    resized(deviceType) {
      // The widths are the minimum width the preview must have. If the preview dom
      // element becomes smaller than the target, it will be scaled down so that the
      // actual width remains the same, and it will preview the correct device.
      const preview = this.$refs.preview
      const previewScaled = this.$refs.previewScaled

      const currentWidth = preview.clientWidth
      const currentHeight = preview.clientHeight
      const targetWidth = deviceType.minWidth
      let scale = 1
      let horizontal = 0
      let vertical = 0

      if (currentWidth < targetWidth) {
        scale = Math.round((currentWidth / targetWidth) * 100) / 100
        horizontal = (currentWidth - currentWidth * scale) / 2 / scale
        vertical = (currentHeight - currentHeight * scale) / 2 / scale
      }

      previewScaled.style.transform = `scale(${scale})`
      previewScaled.style.transformOrigin = `0 0`
      previewScaled.style.width = `${horizontal * 2 + currentWidth}px`
      previewScaled.style.height = `${vertical * 2 + currentHeight}px`
    },
    deleteElement(element) {
      try {
        this.actionDeleteElement({ element })
      } catch (error) {
        notifyIf(error)
      }
    },
    move(element, index, direction) {
      let elementToMoveId = null
      let beforeElementId = null

      if (direction === 'up' && index !== 0) {
        elementToMoveId = element.id
        beforeElementId = this.elements[index - 1].id
      } else if (direction === 'down' && index !== this.elements.length - 1) {
        elementToMoveId = this.elements[index + 1].id
        beforeElementId = element.id
      }

      // If either is null then we are on the top or bottom end of the elements
      // and therefore the element can't be moved anymore
      if (elementToMoveId === null || beforeElementId === null) {
        return
      }

      try {
        this.actionMoveElement({
          pageId: this.page.id,
          elementId: elementToMoveId,
          beforeElementId,
        })
      } catch (error) {
        notifyIf(error)
      }
    },
    insert(element, index, direction) {
      this.beforeId =
        direction === 'top' ? element.id : this.elements[index + 1]?.id
      this.$refs.addElementModal.show()
    },
    async addElement(elementType) {
      try {
        await this.actionCreateElement({
          page: this.page,
          elementType,
          beforeId: this.beforeId,
        })
        this.$refs.addElementModal.hide()
      } catch (error) {
        notifyIf(error)
      }
    },
  },
}
</script>
