<template>
  <Context>
    <KanbanViewOptionForm ref="form" @submitted="submit">
    </KanbanViewOptionForm>

    <template #footer>
      <div class="context__form-actions">
        <button
          class="button"
          :class="{ 'button--loading': loading }"
          :disabled="loading"
          @click="$refs.form.submit($refs.form.values)"
        >
          {{ $t('action.create') }}
        </button>
      </div>
    </template>
  </Context>
</template>

<script>
import { notifyIf } from '@baserow/modules/core/utils/error'
import context from '@baserow/modules/core/mixins/context'
import KanbanViewOptionForm from '@baserow_premium/components/views/kanban/KanbanViewOptionForm'

export default {
  name: 'KanbanViewCreateStackContext',
  components: { KanbanViewOptionForm },
  mixins: [context],
  props: {
    fields: {
      type: Array,
      required: true,
    },
    storePrefix: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      loading: false,
    }
  },
  methods: {
    async submit(values) {
      this.loading = true

      try {
        await this.$store.dispatch(
          this.storePrefix + 'view/kanban/createStack',
          {
            fields: this.fields,
            color: values.color,
            value: values.value,
          }
        )
        this.$refs.form.reset()
        this.hide()
      } catch (error) {
        notifyIf(error, 'field')
      }

      this.loading = false
    },
  },
}
</script>
