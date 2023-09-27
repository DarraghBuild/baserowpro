<template>
  <div>
    <Dropdown
      :value="workflowActionType"
      :show-search="false"
      @change="$emit('type-changed', $event)"
    >
      <DropdownItem
        v-for="availableWorkflowActionType in availableWorkflowActionTypes"
        :key="availableWorkflowActionType.getType()"
        :name="availableWorkflowActionType.label"
        :value="availableWorkflowActionType"
      ></DropdownItem>
    </Dropdown>
    <component :is="workflowActionType.form" class="margin-top-2"></component>
  </div>
</template>

<script>
export default {
  name: 'WorkflowAction',
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
