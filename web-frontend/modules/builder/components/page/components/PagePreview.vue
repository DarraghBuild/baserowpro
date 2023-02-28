<template>
  <div class="page-preview__wrapper">
    <div
      ref="preview"
      class="page-preview"
      :class="{
        'page-preview--tablet': device == 'tablet',
        'page-preview--smartphone': device == 'smartphone',
      }"
    >
      <div ref="previewScaled" class="page-preview__scaled">Preview</div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PagePreview',
  data() {
    return {
      device: '',
    }
  },
}
</script>
