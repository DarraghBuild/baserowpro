<template functional>
  <div class="card-file__list-wrapper">
    <ul class="card-file__list">
      <li class="card-file__item">
        <img
          v-if="props.value?.is_image"
          class="card-file__image"
          :src="props.value?.thumbnails?.tiny?.url"
        />
        <i
          v-else
          class="fas card-file__icon"
          :class="'fa-' + $options.methods.getIconClass(props.value.mime_type)"
        ></i>
      </li>
    </ul>
  </div>
</template>

<script>
import { mimetype2fa } from '@baserow/modules/core/utils/fontawesome'

export default {
  height: 22,
  name: 'RowCardFieldSingleFile',
  methods: {
    getIconClass(mimeType) {
      return mimetype2fa(mimeType)
    },
  },
}
</script>
