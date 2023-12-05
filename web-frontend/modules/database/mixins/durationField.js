import {
  formatDuration,
  guessDurationValue,
} from '@baserow/modules/core/utils/duration'

/**
 * This mixin contains some method overrides for validating and formatting the
 * duration field. This mixin is used in both the GridViewFieldDuration and
 * RowEditFieldDuration components.
 */
export default {
  methods: {
    formatValue(value, format) {
      return formatDuration(value, format)
    },
    beforeSave(value) {
      return guessDurationValue(value, this.field.duration_format)
    },
  },
}
