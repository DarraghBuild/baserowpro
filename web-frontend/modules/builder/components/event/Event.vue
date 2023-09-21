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
      <WorkflowAction />
    </template>
  </Expandable>
</template>

<script>
import { Event } from '@baserow/modules/builder/eventTypes'
import WorkflowAction from '@baserow/modules/core/components/workflowActions/WorkflowAction.vue'

export default {
  name: 'Event',
  components: { WorkflowAction },
  props: {
    event: {
      type: Event,
      required: true,
    },
  },
  methods: {
    getIcon(expanded) {
      return expanded ? 'fa-chevron-down' : 'fa-chevron-right'
    },
  },
}
</script>
