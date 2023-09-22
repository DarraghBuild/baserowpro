<template>
  <div>
    <Event
      v-for="event in elementType.getEvents()"
      :key="event.getType()"
      :event="event"
      :available-workflow-actions="availableWorkflowActions"
      class="margin-bottom-2"
    ></Event>
  </div>
</template>

<script>
import elementSidePanel from '@baserow/modules/builder/mixins/elementSidePanel'
import Event from '@baserow/modules/builder/components/event/Event.vue'

export default {
  name: 'EventSidePanel',
  components: { Event },
  mixins: [elementSidePanel],
  computed: {
    availableWorkflowActions() {
      return Object.values(this.$registry.getAll('workflowAction'))
    },
  },
}
</script>
