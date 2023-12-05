<template>
  <div
    class="grid-view__cell active"
    :class="{
      editing: editing,
      invalid: editing && !isValid(),
    }"
    @contextmenu="stopContextIfEditing($event)"
  >
    <div v-show="!editing" class="grid-field-duration">
      {{ formattedValue }}
    </div>
    <template v-if="editing">
      <input
        ref="input"
        v-model="copy"
        type="text"
        class="grid-field-duration__input"
      />
      <div v-show="!isValid()" class="grid-view__cell--error align-right">
        {{ getError() }}
      </div>
    </template>
  </div>
</template>

<script>
import gridField from '@baserow/modules/database/mixins/gridField'
import gridFieldInput from '@baserow/modules/database/mixins/gridFieldInput'
import durationField from '@baserow/modules/database/mixins/durationField'

export default {
  mixins: [gridField, gridFieldInput, durationField],
  computed: {
    formattedValue() {
      return this.value !== null
        ? this.formatValue(this.value, this.field.duration_format)
        : ''
    },
  },
  methods: {
    edit(value = null, event = null) {
      // value is null when the user double clicks on the cell to edit it or
      // when the user presses the enter key to edit it. The value is undefined
      // when the user clicks only once on the cell and then presses the keys to
      // replace the value.
      const valueToEdit = value === null ? this.formattedValue : ''
      return this.$super(gridFieldInput).edit(valueToEdit, event)
    },
    afterEdit() {
      this.$nextTick(() => {
        this.$refs.input.focus()
        this.$refs.input.selectionStart = this.$refs.input.selectionEnd = 100000
      })
    },
  },
}
</script>
