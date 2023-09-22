<template>
  <div>
    <Dropdown v-model="workflowActionSelected" :show-search="false">
      <DropdownItem
        v-for="workflowAction in availableWorkflowActions"
        :key="workflowAction.type"
        :name="workflowAction.label"
        :value="workflowAction"
      ></DropdownItem>
    </Dropdown>
    <component
      :is="workflowActionSelected.form"
      v-if="workflowActionSelected"
      class="margin-top-2"
    ></component>
  </div>
</template>

<script>
export default {
  name: 'WorkflowAction',
  props: {
    availableWorkflowActions: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      workflowActionSelected: null,
    }
  },
}
</script>
