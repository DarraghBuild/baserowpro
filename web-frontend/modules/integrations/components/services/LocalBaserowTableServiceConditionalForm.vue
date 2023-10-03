<template>
  <div>
    <div v-if="!dataSourceFilteringPermitted">
      <p>
        {{
          $t(
            'localBaserowTableServiceConditionalForm.noTableChosenForFiltering'
          )
        }}
      </p>
    </div>
    <div v-if="dataSourceFilteringPermitted && dataSource.filters.length === 0">
      <div class="filters__none">
        <div class="filters__none-title">
          {{ $t('localBaserowTableServiceConditionalForm.noFilterTitle') }}
        </div>
        <div class="filters__none-description">
          {{ $t('localBaserowTableServiceConditionalForm.noFilterText') }}
        </div>
      </div>
    </div>
    <ViewFieldConditionsForm
      v-if="dataSourceFilteringPermitted"
      :filters="getSortedDataSourceFilters()"
      :disable-filter="false"
      :filter-type="dataSource.filter_type"
      :fields="dataSourceFields"
      :read-only="false"
      class="filters__items"
      @deleteFilter="deleteFilter($event)"
      @updateFilter="updateFilter($event)"
      @selectOperator="$emit('values-changed', { filter_type: $event })"
    />
    <div v-if="dataSourceFilteringPermitted" class="filters_footer">
      <a class="filters__add" @click.prevent="addFilter()">
        <i class="filters__add-icon iconoir-plus"></i>
        {{ $t('localBaserowTableServiceConditionalForm.addFilter') }}</a
      >
    </div>
  </div>
</template>

<script>
import ViewFieldConditionsForm from '@baserow/modules/database/components/view/ViewFieldConditionsForm.vue'
import { hasCompatibleFilterTypes } from '@baserow/modules/database/utils/field'
import { notifyIf } from '@baserow/modules/core/utils/error'

export default {
  name: 'LocalBaserowTableServiceConditionalForm',
  components: {
    ViewFieldConditionsForm,
  },
  props: {
    dataSource: {
      type: Object,
      required: true,
    },
  },
  computed: {
    /*
     * Responsible for informing whether the data source is ready
     * for filters or not - for now, we just need a `table_id`.
     */
    dataSourceFilteringPermitted() {
      return this.dataSource.table_id !== null
    },
    filterTypes() {
      return this.$registry.getAll('viewFilter')
    },
    /*
     * Responsible for finding all field metadata in the schema.
     * This will be used by the `ViewFieldConditionsForm` component
     * to display the filters applicable for each field type.
     */
    dataSourceFields() {
      const schema = this.dataSource.schema
      if (schema === null) {
        return []
      }
      const schemaProperties =
        schema.type === 'array' ? schema.items : schema.properties
      return Object.values(schemaProperties).map((prop) => prop.metadata)
    },
  },
  methods: {
    /*
     * Responsible for returning the first compatible field we have in
     * our schema fields. Used by `addFilter` to decide what the newly
     * added filter's field should be.
     */
    getFirstCompatibleField(fields) {
      return fields
        .slice()
        .sort((a, b) => b.primary - a.primary)
        .find((field) => hasCompatibleFilterTypes(field, this.filterTypes))
    },
    /*
     * Responsible for returning all current data source filters, but
     * sorted by their ID. Without the sorting, `ViewFieldConditionsForm`
     * will add/update them in a haphazard way.
     */
    getSortedDataSourceFilters() {
      const dataSourceFilters = [...this.dataSource.filters]
      return dataSourceFilters.sort((a, b) => a.id - b.id)
    },
    /*
     * Responsible for asynchronously adding a new data source filter.
     * By default it'll be for the first compatible field, of type equal,
     * and value blank.
     */
    async addFilter() {
      try {
        const field = this.getFirstCompatibleField(this.dataSourceFields)
        if (field === undefined) {
          await this.$store.dispatch('toast/error', {
            title: this.$t(
              'localBaserowTableServiceConditionalForm.noCompatibleFilterTypesErrorTitle'
            ),
            message: this.$t(
              'localBaserowTableServiceConditionalForm.noCompatibleFilterTypesErrorMessage'
            ),
          })
        } else {
          const newFilters = [...this.dataSource.filters]
          newFilters.push({
            field: field.id,
            type: 'equal',
            value: '',
            service: this.dataSource.service_id,
          })
          this.$emit('values-changed', {
            filters: newFilters,
          })
        }
      } catch (error) {
        notifyIf(error, 'dataSource')
      }
    },
    /*
     * Responsible for removing the chosen filter from the data source's filters.
     */
    deleteFilter(filter) {
      const newFilters = this.dataSource.filters.filter(({ id }) => {
        return id !== filter.id
      })
      this.$emit('values-changed', {
        filters: newFilters,
      })
    },
    /*
     * Responsible for updating the chosen filter in the data source's filters.
     */
    updateFilter({ filter, values }) {
      const newFilters = this.dataSource.filters.map((filterConf) => {
        if (filterConf.id === filter.id) {
          return { ...filterConf, ...values }
        }
        return filterConf
      })
      this.$emit('values-changed', {
        filters: newFilters,
      })
    },
  },
}
</script>
