<template>
  <ApplicationBuilderFormulaInputGroup
    v-model="fieldValue"
    :placeholder="$t('upsertRowWorkflowActionForm.fieldMappingPlaceholder')"
    :data-providers-allowed="DATA_PROVIDERS_ALLOWED_ELEMENTS"
    :label="field.name"
  />
</template>

<script>
import ApplicationBuilderFormulaInputGroup from '@baserow/modules/builder/components/ApplicationBuilderFormulaInputGroup'
import { DATA_PROVIDERS_ALLOWED_ELEMENTS } from '@baserow/modules/builder/enums'

export default {
  name: 'FieldMapping',
  components: { ApplicationBuilderFormulaInputGroup },
  props: {
    field: {
      type: Object,
      required: true,
    },
    value: {
      type: String,
      required: false,
      default: () => '',
    },
  },
  computed: {
    DATA_PROVIDERS_ALLOWED_ELEMENTS() {
      return DATA_PROVIDERS_ALLOWED_ELEMENTS
    },
    fieldValue: {
      get() {
        return this.value
      },
      set(value) {
        this.$emit('change', value)
      },
    },
  },
}
</script>
