<template functional>
  <div ref="cell" class="grid-view__cell" :class="data.staticClass || ''">
    <div v-if="props.value" class="grid-field-duration">
      {{
        $options.methods.formatDurationValue(
          props.value,
          props.field.duration_format
        )
      }}
    </div>
    <div v-else class="grid-field-duration-placeholder">
      {{ props.field.duration_format }}
    </div>
  </div>
</template>

<script>
import { formatDuration } from '@baserow/modules/core/utils/duration'

export default {
  name: 'FunctionalGridViewFieldDuration',
  functional: true,
  props: {
    value: {
      required: false,
      type: Number,
      default: null,
    },
    field: {
      required: true,
      type: Object,
    },
  },
  methods: {
    formatDurationValue(value, format) {
      return formatDuration(value, format)
    },
  },
}
</script>
