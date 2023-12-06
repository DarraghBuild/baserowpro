import {
  formatDuration,
  guessDurationValueFromString,
  roundDurationValueToFormat,
} from '@baserow/modules/core/utils/duration'

/**
 * This mixin contains some method overrides for validating and formatting the
 * duration field. This mixin is used in both the GridViewFieldDuration and
 * RowEditFieldDuration components.
 */
export default {
  methods: {
    formatValue(field, value) {
      return formatDuration(field, value)
    },
    beforeSave(inputValue) {
      let value = guessDurationValueFromString(inputValue)
      if (value !== null) {
        value = roundDurationValueToFormat(this.field, value)
      }
      return value
    },
  },
}
