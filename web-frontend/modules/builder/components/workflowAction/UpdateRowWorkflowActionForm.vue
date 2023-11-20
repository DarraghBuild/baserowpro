<template>
  <form @submit.prevent="submit">
    <UpsertRowWorkflowActionForm
      enable-row-id
      :workflow-action="workflowAction"
      :default-values="defaultValues"
      @values-changed="$emit('values-changed', $event)"
    >
    </UpsertRowWorkflowActionForm>
  </form>
</template>

<script>
import UpsertRowWorkflowActionForm from '@baserow/modules/builder/components/workflowAction/UpsertRowWorkflowActionForm'
import form from '@baserow/modules/core/mixins/form'

export default {
  name: 'UpdateRowWorkflowActionForm',
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
