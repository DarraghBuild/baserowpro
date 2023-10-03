<template>
  <form @submit.prevent>
    <div class="row">
      <div class="col col-12">
        <LocalBaserowTableSelector
          v-model="values.table_id"
          :databases="databases"
          :view-id.sync="values.view_id"
        ></LocalBaserowTableSelector>
      </div>
    </div>
    <div class="row">
      <div class="col col-12">
        <Tabs>
          <Tab
            :title="$t('localBaserowListRowsForm.filterTabTitle')"
            class="data-source-form__condition-form-tab"
          >
            <LocalBaserowTableServiceConditionalForm
              v-if="values.table_id && dataSource.schema"
              v-model="values.filters"
              :schema="dataSource.schema"
              :filter-type.sync="values.filter_type"
            />
            <p v-if="!values.table_id">
              {{ $t('localBaserowListRowsForm.noTableChosenForFiltering') }}
            </p>
          </Tab>
          <Tab
            :title="$t('localBaserowListRowsForm.sortTabTitle')"
            class="data-source-form__sort-form-tab"
          >
            <LocalBaserowTableServiceSortForm
              v-if="values.table_id && dataSource.schema"
              v-model="values.sortings"
              :schema="dataSource.schema"
            ></LocalBaserowTableServiceSortForm>
            <p v-if="!values.table_id">
              {{ $t('localBaserowListRowsForm.noTableChosenForSorting') }}
            </p>
          </Tab>
          <Tab :title="$t('localBaserowListRowsForm.searchTabTitle')">
            <FormInput
              v-model="values.search_query"
              type="text"
              small-label
              :placeholder="
                $t('localBaserowListRowsForm.searchFieldPlaceHolder')
              "
            />
          </Tab>
        </Tabs>
      </div>
    </div>
  </form>
</template>

<script>
import _ from 'lodash'
import form from '@baserow/modules/core/mixins/form'
import LocalBaserowTableSelector from '@baserow/modules/integrations/components/services/LocalBaserowTableSelector'
import LocalBaserowTableServiceConditionalForm from '@baserow/modules/integrations/components/services/LocalBaserowTableServiceConditionalForm.vue'
import LocalBaserowTableServiceSortForm from '@baserow/modules/integrations/components/services/LocalBaserowTableServiceSortForm'

export default {
  components: {
    LocalBaserowTableSelector,
    LocalBaserowTableServiceSortForm,
    LocalBaserowTableServiceConditionalForm,
  },
  mixins: [form],
  props: {
    builder: {
      type: Object,
      required: true,
    },
    dataSource: {
      type: Object,
      required: true,
    },
    contextData: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      allowedValues: [
        'table_id',
        'view_id',
        'search_query',
        'filters',
        'filter_type',
        'sortings',
      ],
      values: {
        table_id: null,
        view_id: null,
        search_query: '',
        filters: [],
        sortings: [],
        filter_type: 'AND',
      },
    }
  },
  computed: {
    databases() {
      return this.contextData?.databases || []
    },
    filtersAndSorts() {
      const defaultValues = this.getDefaultValues()
      return [defaultValues.filters, defaultValues.sortings]
    },
  },
  watch: {
    filtersAndSorts(newValue) {
      if (!_.isEqual(newValue[0], this.values.filters)) {
        this.values.filters = newValue[0]
      }
      if (!_.isEqual(newValue[1], this.values.sortings)) {
        this.values.sortings = newValue[1]
      }
    },
  },
}
</script>
