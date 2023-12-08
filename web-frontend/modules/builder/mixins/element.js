import { ClickEvent } from '@baserow/modules/builder/eventTypes'
import ResolveFormulaMixin from '@baserow/modules/builder/mixins/resolveFormula'

export default {
  mixins: [ResolveFormulaMixin],
  inject: ['builder', 'page', 'mode'],
  props: {
    element: {
      type: Object,
      required: true,
    },
  },
  computed: {
    elementType() {
      return this.$registry.get('element', this.element.type)
    },
    isEditable() {
      return this.mode === 'editing'
    },
    applicationContext() {
      return {
        builder: this.builder,
        page: this.page,
        mode: this.mode,
        element: this.element,
      }
    },
  },
  methods: {
    fireEvent(EventType) {
      if (this.mode !== 'editing') {
        const workflowActions = this.$store.getters[
          'workflowAction/getElementWorkflowActions'
        ](this.page, this.element.id)

        new EventType(this).fire({
          workflowActions,
          resolveFormula: this.resolveFormula,
          applicationContext: this.applicationContext,
        })
      }
    },
    fireClickEvent() {
      this.fireEvent(ClickEvent)
    },
  },
}
