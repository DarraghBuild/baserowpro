<template functional>
  <div class="grid-view__cell grid-field-file__cell">
    <div v-if="props.value" class="grid-field-file__item">
      <a class="grid-field-file__link">
        <img
          v-if="props.value.is_image"
          class="grid-field-file__image"
          :src="props.value?.thumbnails?.tiny?.url"
        />
        <i
          v-else
          class="fas grid-field-file__icon"
          :class="'fa-' + $options.methods.getIconClass(props.value.mime_type)"
        ></i>
      </a>
    </div>
  </div>
</template>

<script>
import { mimetype2fa } from '@baserow/modules/core/utils/fontawesome'

export default {
  name: 'FunctionalGridViewSingleFile',
  methods: {
    getIconClass(mimeType) {
      return mimetype2fa(mimeType)
    },
  },
}
</script>
