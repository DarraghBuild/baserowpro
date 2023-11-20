<template>
  <form @submit.prevent @keydown.enter.prevent>
    <ApplicationBuilderFormulaInputGroup
      v-model="values.value"
      :placeholder="$t('upsertRowWorkflowActionForm.fieldMappingPlaceholder')"
      :data-providers-allowed="dataProvidersAllowed"
      :label="field.name"
    />
  </form>
</template>

<script>
import workflowActionForm from '@baserow/modules/builder/mixins/workflowActionForm'
import ApplicationBuilderFormulaInputGroup from '@baserow/modules/builder/components/ApplicationBuilderFormulaInputGroup'

export default {
  name: 'FieldMapping',
  components: { ApplicationBuilderFormulaInputGroup },
  mixins: [workflowActionForm],
  props: {
    field: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      values: {
        value: '',
      },
    }
  },
}
</script>
