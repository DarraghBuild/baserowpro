import { guessDurationValue } from '@baserow/modules/core/utils/string'

/**
 * This mixin contains some method overrides for validating and formatting the
 * duration field. This mixin is used in both the GridViewFieldDuration and
 * RowEditFieldDuration components.
 */
export default {
  methods: {
    beforeSave(value) {
      return guessDurationValue(value, this.field.duration_format)
    },
  },
}
