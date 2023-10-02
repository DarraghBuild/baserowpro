<template>
  <Expandable toggle-on-click>
    <template #header="{ toggle, expanded }">
      <div class="event__header">
        <div class="event__label">{{ event.label }}</div>
        <a class="event__toggle" @click.stop="toggle">
          <i :class="getIcon(expanded)"></i>
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
        @delete="deleteWorkflowAction(workflowAction)"
        @update="updateWorkflowAction(workflowAction, $event)"
      />
      <div class="margin-top-2">
        <a
          v-if="!addingElement"
          class="anchor event__add-element"
          @click="addWorkflowAction"
        >
          <i class="iconoir-plus margin-right-1"></i>
          {{ $t('event.addAction') }}
        </a>
        <div v-else class="loading"></div>
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
import _ from 'lodash'

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
  data() {
    return {
      addingElement: false,
    }
  },
  methods: {
    ...mapActions({
      actionCreateWorkflowAction: 'workflowAction/create',
      actionDeleteWorkflowAction: 'workflowAction/delete',
      actionUpdateWorkflowAction: 'workflowAction/update',
    }),
    getIcon(expanded) {
      return expanded ? 'iconoir-nav-arrow-down' : 'iconoir-nav-arrow-right'
    },
    async addWorkflowAction() {
      this.addingElement = true
      try {
        await this.actionCreateWorkflowAction({
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
      this.addingElement = false
    },
    deleteWorkflowAction(workflowAction) {
      try {
        this.actionDeleteWorkflowAction({ page: this.page, workflowAction })
      } catch (error) {
        notifyIf(error)
      }
    },
    updateWorkflowAction(workflowAction, values) {
      // In this case there weren't any actual changes
      if (_.isMatch(workflowAction, values)) {
        return
      }

      try {
        this.actionUpdateWorkflowAction({
          page: this.page,
          workflowAction,
          values,
        })
      } catch (error) {
        notifyIf(error)
      }
    },
  },
}
</script>
