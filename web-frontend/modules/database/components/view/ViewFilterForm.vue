<template>
  <div>
    <div v-if="view.filters.length === 0">
      <div class="filters__none">
        <div class="filters__none-title">
          {{ $t('viewFilterContext.noFilterTitle') }}
        </div>
        <div class="filters__none-description">
          {{ $t('viewFilterContext.noFilterText') }}
        </div>
      </div>
    </div>
    <ViewFieldConditionsForm
      :filters="view.filters"
      :disable-filter="disableFilter"
      :filter-type="view.filter_type"
      :fields="fields"
      :view="view"
      :read-only="readOnly"
      :dropdown-target="dropdownTarget"
      class="filters__items"
      @deleteFilter="deleteFilter($event)"
      @updateFilter="updateFilter($event)"
      @selectOperator="updateView(view, { filter_type: $event })"
      @dropdown-open="$emit('dropdown-open')"
      @dropdown-closed="$emit('dropdown-closed')"
    />
  </div>
</template>

<script>
import { notifyIf } from '@baserow/modules/core/utils/error'
import ViewFieldConditionsForm from '@baserow/modules/database/components/view/ViewFieldConditionsForm'

export default {
  name: 'ViewFilterForm',
  components: {
    ViewFieldConditionsForm,
  },
  props: {
    fields: {
      type: Array,
      required: true,
    },
    view: {
      type: Object,
      required: true,
    },
    readOnly: {
      type: Boolean,
      required: true,
    },
    disableFilter: {
      type: Boolean,
      required: true,
    },
    dropdownTarget: {
      type: Object,
      required: false,
      default: null,
    },
  },
  methods: {
    async deleteFilter(filter) {
      try {
        await this.$store.dispatch('view/deleteFilter', {
          view: this.view,
          filter,
          readOnly: this.readOnly,
        })
        this.$emit('changed')
      } catch (error) {
        notifyIf(error, 'view')
      }
    },
    /**
     * Updates a filter with the given values. Some data manipulation will also be done
     * because some filter types are not compatible with certain field types.
     */
    async updateFilter({ filter, values }) {
      try {
        await this.$store.dispatch('view/updateFilter', {
          filter,
          values,
          readOnly: this.readOnly,
        })
        this.$emit('changed')
      } catch (error) {
        notifyIf(error, 'view')
      }
    },
  },
}
</script>
