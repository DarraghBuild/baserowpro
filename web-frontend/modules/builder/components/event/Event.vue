<template>
  <Expandable toggle-on-click>
    <template #header="{ toggle, expanded }">
      <div class="event__header">
        <div class="event__label">{{ event.label }}</div>
        <a class="event__toggle" @click.stop="toggle">
          <i class="fas" :class="getIcon(expanded)"></i>
        </a>
      </div>
    </template>
    <template #default>
      <WorkflowAction
        v-for="workflowAction in workflowActions"
        :key="workflowAction.id"
        class="margin-top-2"
        :available-workflow-action-types="availableWorkflowActionTypes"
        :workflow-action="workflowAction"
        @type-changed="workflowActionTypeChanged(workflowAction, $event)"
        @delete="deleteWorkflowAction(workflowAction)"
      />
      <div class="margin-top-2">
        <a class="anchor" @click="addWorkflowAction">
          <i class="fas fa-plus margin-right-1"></i>
          {{ $t('event.addAction') }}
        </a>
      </div>
    </template>
  </Expandable>
</template>

<script>
import { Event } from '@baserow/modules/builder/eventTypes'
import WorkflowAction from '@baserow/modules/core/components/workflowActions/WorkflowAction.vue'
import { NotificationWorkflowActionType } from '@baserow/modules/builder/workflowActionTypes'
import { mapActions } from 'vuex'
import { notifyIf } from '@baserow/modules/core/utils/error'

const DEFAULT_WORKFLOW_ACTION_TYPE = NotificationWorkflowActionType.getType()

export default {
  name: 'Event',
  components: { WorkflowAction },
  inject: ['page'],
  props: {
    event: {
      type: Event,
      required: true,
    },
    element: {
      type: Object,
      required: true,
    },
    workflowActions: {
      type: Array,
      required: false,
      default: () => [],
    },
    availableWorkflowActionTypes: {
      type: Array,
      required: true,
    },
  },
  methods: {
    ...mapActions({
      actionCreateWorkflowAction: 'workflowAction/create',
      actionDeleteWorkflowAction: 'workflowAction/delete',
    }),
    getIcon(expanded) {
      return expanded ? 'fa-chevron-down' : 'fa-chevron-right'
    },
    addWorkflowAction() {
      try {
        this.actionCreateWorkflowAction({
          page: this.page,
          workflowActionType: DEFAULT_WORKFLOW_ACTION_TYPE,
          eventType: this.event.getType(),
          configuration: {
            element_id: this.element.id,
          },
        })
      } catch (error) {
        notifyIf(error)
      }
    },
    deleteWorkflowAction(workflowAction) {
      try {
        this.actionDeleteWorkflowAction({ page: this.page, workflowAction })
      } catch (error) {
        notifyIf(error)
      }
    },
    workflowActionTypeChanged(workflowAction, newType) {
      console.log(workflowAction, newType)
    },
  },
}
</script>
