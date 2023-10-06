<template>
  <form @submit.prevent>
    <div>
      <div class="row">
        <div class="col col-12">
          <LocalBaserowTableSelector
            v-model="values.table_id"
            class="local-baserow-get-row-form__table-selector"
            :databases="databases"
            :view-id.sync="values.view_id"
          ></LocalBaserowTableSelector>
        </div>
      </div>
      <div class="row">
        <div class="col col-6">
          <ApplicationBuilderFormulaInputGroup
            v-model="values.row_id"
            small-label
            :label="$t('localBaserowGetRowForm.rowFieldLabel')"
            :placeholder="$t('localBaserowGetRowForm.rowFieldPlaceHolder')"
            :data-providers-allowed="DATA_PROVIDERS_ALLOWED_DATA_SOURCES"
          />
        </div>
      </div>
      <div class="row">
        <div class="col col-12">
          <Tabs>
            <Tab
              :title="$t('localBaserowGetRowForm.filterTabTitle')"
              class="data-source-form__condition-form-tab"
            >
              <LocalBaserowTableServiceConditionalForm
                v-if="values.table_id && dataSource.schema"
                v-model="values.filters"
                :schema="dataSource.schema"
                :filter-type.sync="values.filter_type"
              />
              <p v-if="!values.table_id">
                {{ $t('localBaserowGetRowForm.noTableChosenForFiltering') }}
              </p>
            </Tab>
            <Tab :title="$t('localBaserowGetRowForm.searchTabTitle')">
              <FormInput
                v-model="values.search_query"
                type="text"
                small-label
                :placeholder="
                  $t('localBaserowGetRowForm.searchFieldPlaceHolder')
                "
              />
            </Tab>
          </Tabs>
        </div>
      </div>
    </div>
  </form>
</template>

<script>
import form from '@baserow/modules/core/mixins/form'
import { DATA_PROVIDERS_ALLOWED_DATA_SOURCES } from '@baserow/modules/builder/enums'
import ApplicationBuilderFormulaInputGroup from '@baserow/modules/builder/components/ApplicationBuilderFormulaInputGroup'
import LocalBaserowTableSelector from '@baserow/modules/integrations/components/services/LocalBaserowTableSelector'
import LocalBaserowTableServiceConditionalForm from '@baserow/modules/integrations/components/services/LocalBaserowTableServiceConditionalForm.vue'
import _ from 'lodash'

export default {
  components: {
    LocalBaserowTableSelector,
    LocalBaserowTableServiceConditionalForm,
    ApplicationBuilderFormulaInputGroup,
  },
  mixins: [form],
  props: {
    builder: {
      type: Object,
      required: true,
    },
    contextData: {
      type: Object,
      required: false,
      default: () => ({
        databases: [],
      }),
    },
    dataSource: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      allowedValues: [
        'table_id',
        'view_id',
        'row_id',
        'search_query',
        'filters',
        'filter_type',
      ],
      values: {
        table_id: null,
        view_id: null,
        row_id: '',
        search_query: '',
        filters: [],
        filter_type: 'AND',
      },
    }
  },
  computed: {
    storeFilters() {
      return this.getDefaultValues().filters
    },
    DATA_PROVIDERS_ALLOWED_DATA_SOURCES: () =>
      DATA_PROVIDERS_ALLOWED_DATA_SOURCES,
    databases() {
      return this.contextData?.databases || []
    },
  },
  watch: {
    storeFilters(newValue) {
      if (!_.isEqual(newValue, this.values.filters)) {
        this.values.filters = newValue
      }
    },
  },
}
</script>
