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
          v-for="element in elements"
          :key="element.id"
          :element="element"
          :active="element.id === elementActiveId"
          @selected="elementActiveId = element.id"
          @delete="deleteElement(element)"
          @move="move(element, $event)"
        />
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import Element from '@baserow/modules/builder/components/page/Element'
import { notifyIf } from '@baserow/modules/core/utils/error'

export default {
  name: 'PagePreview',
  components: { Element },
  data() {
    return {
      elementActiveId: null,
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
    move(element, direction) {
      try {
        this.actionMoveElement({
          pageId: this.page.id,
          elementId: element.id,
          direction,
        })
      } catch (error) {
        notifyIf(error)
      }
    },
  },
}
</script>
