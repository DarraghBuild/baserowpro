<template>
  <div>
    <label class="control__label control__label--small">{{
      $t('upsertRowWorkflowActionForm.integrationDropdownLabel')
    }}</label>
    <Dropdown
      v-if="state === 'loaded'"
      v-model="values.integration_id"
      fixed-items
      class="data-source-form__integration-dropdown"
      :placeholder="$t('dataSourceForm.integrationPlaceholder')"
      show-footer
    >
      <DropdownItem
        v-for="integrationItem in integrations"
        :key="integrationItem.id"
        :name="integrationItem.name"
        :value="integrationItem.id"
      />
      <template #emptyState>
        {{ $t('dataSourceForm.noIntegrations') }}
      </template>
      <template #footer>
        <a
          class="select__footer-button"
          @click="$refs.IntegrationCreateEditModal.show()"
        >
          <i class="iconoir-plus"></i>
          {{ $t('dataSourceForm.addIntegration') }}
        </a>
        <IntegrationCreateEditModal
          ref="IntegrationCreateEditModal"
          :application="builder"
          :integration-type="integrationType"
          create
          @created="values.integration_id = $event.id"
        />
      </template>
    </Dropdown>
    <LocalBaserowTableSelector
      v-if="selectedIntegration"
      v-model="values.table_id"
      :databases="databases"
      :display-view-dropdown="false"
      class="margin-top-2"
    ></LocalBaserowTableSelector>
    <ApplicationBuilderFormulaInputGroup
      v-if="enableRowId && values.integration_id"
      v-model="values.row_id"
      small-label
      :placeholder="$t('upsertRowWorkflowActionForm.rowIdPlaceholder')"
      :data-providers-allowed="dataProvidersAllowed"
      :label="$t('upsertRowWorkflowActionForm.rowIdLabel')"
    />
    <template v-if="workflowAction.service && workflowAction.service.schema">
      <FieldMapping
        v-for="field in getWritableServiceFields"
        :key="field.id"
        :field="field"
        :default-values="getFieldMapping(field)"
        @values-changed="updateFieldMapping($event, field.id)"
      ></FieldMapping>
    </template>
  </div>
</template>

<script>
import workflowActionForm from '@baserow/modules/builder/mixins/workflowActionForm'
import LocalBaserowTableSelector from '@baserow/modules/integrations/components/services/LocalBaserowTableSelector.vue'
import IntegrationCreateEditModal from '@baserow/modules/core/components/integrations/IntegrationCreateEditModal.vue'
import { mapActions, mapGetters } from 'vuex'
import { LocalBaserowIntegrationType } from '@baserow/modules/integrations/integrationTypes'
import { notifyIf } from '@baserow/modules/core/utils/error'
import FieldMapping from '@baserow/modules/builder/components/workflowAction/FieldMapping.vue'
import ApplicationBuilderFormulaInputGroup from '@baserow/modules/builder/components/ApplicationBuilderFormulaInputGroup.vue'

export default {
  name: 'UpsertRowWorkflowActionForm',
  components: {
    ApplicationBuilderFormulaInputGroup,
    FieldMapping,
    IntegrationCreateEditModal,
    LocalBaserowTableSelector,
  },
  mixins: [workflowActionForm],
  inject: ['builder'],
  props: {
    workflowAction: {
      type: Object,
      required: false,
      default: null,
    },
    enableRowId: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
  data() {
    return {
      values: {
        row_id: '',
        table_id: null,
        field_mappings: [],
        integration_id: null,
      },
      state: null,
      selectedIntegration: null,
    }
  },
  computed: {
    ...mapGetters({
      integrations: 'integration/getIntegrations',
    }),
    getWritableServiceFields() {
      if (this.workflowAction.service && this.workflowAction.service.schema) {
        const schema = this.workflowAction.service.schema
        const schemaProperties =
          schema.type === 'array' ? schema.items.properties : schema.properties
        return Object.values(schemaProperties)
          .filter(({ metadata }) => metadata && !metadata.read_only)
          .map((prop) => prop.metadata)
      }
      return []
    },
    integrationType() {
      return this.$registry.get(
        'integration',
        LocalBaserowIntegrationType.getType()
      )
    },
    databases() {
      return this.selectedIntegration?.context_data.databases || []
    },
  },
  watch: {
    'values.integration_id'(newVal, oldValue) {
      this.refreshIntegration()
    },
  },
  async created() {
    this.state = 'loading'
    try {
      await Promise.all([
        this.actionFetchIntegrations({
          applicationId: this.builder.id,
        }),
      ])
    } catch (error) {
      notifyIf(error)
    }
    this.refreshIntegration()
    this.state = 'loaded'
  },
  methods: {
    ...mapActions({
      actionFetchIntegrations: 'integration/fetch',
    }),
    getFieldMapping(field) {
      return this.workflowAction.field_mappings.find(
        (fieldMapping) => fieldMapping.field_id === field.id
      )
    },
    updateFieldMapping(event, fieldId) {
      if (this.workflowAction.service == null) {
        return false
      }
      const existingMapping = this.values.field_mappings.some(
        // eslint-disable-next-line camelcase
        ({ field_id }) => field_id === fieldId
      )
      if (existingMapping) {
        const newMapping = this.values.field_mappings.map((fieldMapping) => {
          if (fieldMapping.field_id === fieldId) {
            return { ...fieldMapping, ...event }
          }
          return fieldMapping
        })
        this.values.field_mappings = newMapping
      } else {
        // It already exists
        this.values.field_mappings.push({
          field_id: fieldId,
          ...event,
        })
      }
    },
    refreshIntegration() {
      this.selectedIntegration = this.$store.getters[
        'integration/getIntegrationById'
      ](this.values.integration_id)
    },
  },
}
</script>
