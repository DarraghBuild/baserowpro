<template>
  <div class="control__elements">
    <input
      ref="input"
      v-model="copy"
      type="text"
      class="input field-duration"
      :class="{
        'input--error': (touched && !valid) || isInvalidNumber,
      }"
      :disabled="readOnly"
      @keyup.enter="$refs.input.blur()"
      @focus="select()"
      @blur="unselect()"
    />
    <div v-show="touched && !valid" class="error">
      {{ error }}
    </div>
    <div v-show="isInvalidNumber" class="error">Invalid Number</div>
  </div>
</template>

<script>
import rowEditField from '@baserow/modules/database/mixins/rowEditField'
import rowEditFieldInput from '@baserow/modules/database/mixins/rowEditFieldInput'
import durationField from '@baserow/modules/database/mixins/durationField'
import {
  isValidDuration,
  formatDuration,
} from '@baserow/modules/core/utils/duration'

export default {
  mixins: [rowEditField, rowEditFieldInput, durationField],
  computed: {
    isInvalidDuration() {
      return isValidDuration(this.copy) === false
    },
  },
  watch: {
    'field.duration_format': {
      handler(value) {
        this.copy = this.prepareCopy(value)
      },
    },
  },
  methods: {
    prepareCopy() {
      return formatDuration(this.value, this.field.duration_format)
    },
  },
}
</script>
