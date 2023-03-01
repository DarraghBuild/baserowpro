<template>
  <div class="page-preview__wrapper">
    <div
      v-if="deviceType"
      ref="preview"
      class="page-preview"
      :style="{ 'max-width': maxWidth }"
    >
      <div ref="previewScaled" class="page-preview__scaled">
        <ul>
          <li v-for="element in elements" :key="element.id">
            <Element :element="element" />
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import Element from '@baserow/modules/builder/components/page/Element'

export default {
  name: 'PagePreview',
  components: { Element },
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
  },
}
</script>
