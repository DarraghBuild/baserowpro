<template>
  <UpsertRowWorkflowActionForm
    :workflow-action="workflowAction"
    :default-values="defaultValues"
    @values-changed="$emit('values-changed', $event)"
  >
  </UpsertRowWorkflowActionForm>
</template>

<script>
import UpsertRowWorkflowActionForm from '@baserow/modules/builder/components/workflowAction/UpsertRowWorkflowActionForm'
import form from '@baserow/modules/core/mixins/form'

export default {
  name: 'CreateRowWorkflowActionForm',
  components: { UpsertRowWorkflowActionForm },
  mixins: [form],
  props: {
    workflowAction: {
      type: Object,
      required: false,
      default: null,
    },
  },
  data() {
    return {
      values: {},
    }
  },
}
</script>
