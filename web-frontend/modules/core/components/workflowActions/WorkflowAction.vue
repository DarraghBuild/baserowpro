<template>
  <div>
    <WorkflowActionSelector
      :available-workflow-action-types="availableWorkflowActionTypes"
      :workflow-action="workflowAction"
      @change="$emit('type-changed', $event)"
      @delete="$emit('delete')"
    />
    <component :is="workflowActionType.form" class="margin-top-2"></component>
  </div>
</template>

<script>
import WorkflowActionSelector from '@baserow/modules/core/components/workflowActions/WorkflowActionSelector.vue'

export default {
  name: 'WorkflowAction',
  components: { WorkflowActionSelector },
  props: {
    availableWorkflowActionTypes: {
      type: Array,
      required: true,
    },
    workflowAction: {
      type: Object,
      required: false,
      default: null,
    },
  },
  computed: {
    workflowActionType() {
      return this.availableWorkflowActionTypes.find(
        (workflowActionType) =>
          workflowActionType.getType() === this.workflowAction.type
      )
    },
  },
}
</script>
