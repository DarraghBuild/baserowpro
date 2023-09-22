<template>
  <div>
    <!--
      Here we use the index as key to avoid loosing focus when filter id change.
    -->
    <div
      v-for="(filter, index) in filtersTree.filters"
      :key="index"
      class="filters__item"
      :class="{
        'filters__item--loading': filter._ && filter._.loading,
      }"
    >
      <ViewFilterFormOperator
        :index="index"
        :filter-type="filterType"
        :disable-filter="disableFilter"
        @select-boolean-operator="$emit('selectOperator', $event)"
      />
      <div class="filters__field">
        <Dropdown
          :value="filter.field"
          :disabled="disableFilter"
          :fixed-items="true"
          class="dropdown--tiny"
          @input="updateFilter(filter, { field: $event })"
        >
          <DropdownItem
            v-for="field in fields"
            :key="'field-' + field.id"
            :name="field.name"
            :value="field.id"
            :disabled="!hasCompatibleFilterTypes(field, filterTypes)"
          ></DropdownItem>
        </Dropdown>
      </div>
      <div class="filters__type">
        <Dropdown
          :disabled="disableFilter"
          :value="filter.type"
          :fixed-items="true"
          class="dropdown--tiny"
          @input="updateFilter(filter, { type: $event })"
        >
          <DropdownItem
            v-for="fType in allowedFilters(filterTypes, fields, filter.field)"
            :key="fType.type"
            :name="fType.getName()"
            :value="fType.type"
          ></DropdownItem>
        </Dropdown>
      </div>
      <div class="filters__value">
        <component
          :is="getInputComponent(filter.type, filter.field)"
          v-if="
            fieldIdExists(fields, filter.field) &&
            fieldIsCompatible(filter.type, filter.field)
          "
          :ref="`filter-value-${index}`"
          :filter="filter"
          :view="view"
          :fields="fields"
          :disabled="disableFilter"
          :read-only="readOnly"
          @input="updateFilter(filter, { value: $event })"
        />
        <i
          v-else-if="!fieldIdExists(fields, filter.field)"
          v-tooltip="$t('viewFilterContext.relatedFieldNotFound')"
          class="iconoir-warning-triangle color-error"
        ></i>
        <i
          v-else-if="!fieldIsCompatible(filter.type, filter.field)"
          v-tooltip="$t('viewFilterContext.filterTypeNotFound')"
          class="iconoir-warning-triangle color-error"
        ></i>
      </div>
      <a
        v-if="!disableFilter"
        class="filters__remove"
        @click="deleteFilter($event, filter)"
      >
        <i class="fas fa-trash"></i>
      </a>
      <span v-else class="filters__remove"></span>
    </div>
    <div
      v-for="(groupNode, groupIndex) in filtersTree.groups"
      :key="filtersTree.filters.length + groupIndex"
      class="filters__group-item"
      :class="{
        'filters__item--loading': groupNode._ && groupNode._.loading,
      }"
    >
      <ViewFilterFormOperator
        :index="filtersTree.filters.length + groupIndex"
        :filter-type="filterType"
        :disable-filter="disableFilter"
        @select-boolean-operator="$emit('selectOperator', $event)"
      />
      <div class="filters__group-filters">
        <div
          v-for="(filter, index) in groupNode.filters"
          :key="`${groupIndex}-${index}`"
          class="filters__item"
          :class="{
            'filters__item--loading': filter._ && filter._.loading,
          }"
        >
          <ViewFilterFormOperator
            :index="index"
            :filter-type="groupNode.group.filter_type"
            :disable-filter="disableFilter"
            @select-boolean-operator="
              $emit('selectFilterGroupOperator', {
                value: $event,
                filterGroup: groupNode.group,
              })
            "
          />
          <div class="filters__field">
            <Dropdown
              :value="filter.field"
              :disabled="disableFilter"
              :fixed-items="true"
              class="dropdown--tiny"
              @input="updateFilter(filter, { field: $event })"
            >
              <DropdownItem
                v-for="field in fields"
                :key="'field-' + field.id"
                :name="field.name"
                :value="field.id"
                :disabled="!hasCompatibleFilterTypes(field, filterTypes)"
              ></DropdownItem>
            </Dropdown>
          </div>
          <div class="filters__type">
            <Dropdown
              :disabled="disableFilter"
              :value="filter.type"
              :fixed-items="true"
              class="dropdown--tiny"
              @input="updateFilter(filter, { type: $event })"
            >
              <DropdownItem
                v-for="fType in allowedFilters(
                  filterTypes,
                  fields,
                  filter.field
                )"
                :key="fType.type"
                :name="fType.getName()"
                :value="fType.type"
              ></DropdownItem>
            </Dropdown>
          </div>
          <div class="filters__value">
            <component
              :is="getInputComponent(filter.type, filter.field)"
              v-if="
                fieldIdExists(fields, filter.field) &&
                fieldIsCompatible(filter.type, filter.field)
              "
              :ref="`filter-value-${index}`"
              :filter="filter"
              :view="view"
              :fields="fields"
              :disabled="disableFilter"
              :read-only="readOnly"
              @input="updateFilter(filter, { value: $event })"
            />
            <i
              v-else-if="!fieldIdExists(fields, filter.field)"
              v-tooltip="$t('viewFilterContext.relatedFieldNotFound')"
              class="fas fa-exclamation-triangle color-error"
            ></i>
            <i
              v-else-if="!fieldIsCompatible(filter.type, filter.field)"
              v-tooltip="$t('viewFilterContext.filterTypeNotFound')"
              class="fas fa-exclamation-triangle color-error"
            ></i>
          </div>
          <a
            v-if="!disableFilter"
            class="filters__remove"
            @click="deleteFilter($event, filter)"
          >
            <i class="fas fa-trash"></i>
          </a>
          <span v-else class="filters__remove"></span>
        </div>
        <div>
          <a
            class="filters__add"
            @click.prevent="$emit('addFilter', groupNode.group.id)"
          >
            <i class="fas fa-plus"></i>
            {{ $t('viewFilterContext.addFilter') }}</a
          >
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { hasCompatibleFilterTypes } from '@baserow/modules/database/utils/field'
import ViewFilterFormOperator from '@baserow/modules/database/components/view/ViewFilterFormOperator'

const GroupNode = class {
  constructor(group, parent = null) {
    this.group = group
    this.parent = parent
    this.groups = []
    this.filters = []
    if (parent) {
      parent.groups.push(this)
    }
  }

  findGroup(id) {
    if (this.group && this.group.id === id) {
      return this
    }
    for (const group of this.groups) {
      const found = group.findGroup(id)
      if (found) {
        return found
      }
    }
    return null
  }

  addFilter(filter) {
    this.filters.push(filter)
  }

  remove() {
    if (this.parent) {
      this.parent.groups = this.parent.groups.filter((g) => g !== this)
    }
  }
}

export default {
  name: 'ViewFieldConditionsForm',
  components: {
    ViewFilterFormOperator,
  },
  props: {
    filters: {
      type: Array,
      required: true,
    },
    filterGroups: {
      type: Array,
      required: false,
      default: () => [],
    },
    disableFilter: {
      type: Boolean,
      required: true,
    },
    filterType: {
      type: String,
      required: true,
    },
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
  },
  data() {
    return {
      groups: {},
    }
  },
  computed: {
    filterTypes() {
      return this.$registry.getAll('viewFilter')
    },
    localFilters() {
      // Copy the filters
      return [...this.filters]
    },
    filtersTree() {
      const root = new GroupNode(null)
      const groups = { '': root }
      for (const filterGroup of this.filterGroups) {
        const parentId = filterGroup.parent || ''
        const parent = groups[parentId]
        const node = new GroupNode(filterGroup, parent)
        groups[filterGroup.id] = node
      }
      for (const filter of this.filters) {
        const groupId = filter.filter_group != null ? filter.filter_group : ''
        const group = groups[groupId]
        if (group) {
          group.addFilter(filter)
        }
      }
      return root
    },
  },
  watch: {
    /**
     * When a filter has been created or removed we want to focus on last value. By
     * watching localFilters instead of filters, the new and old values are differents.
     */
    localFilters(value, old) {
      if (value.length !== old.length) {
        this.$nextTick(() => {
          this.focusValue(value.length - 1)
        })
      }
    },
  },
  methods: {
    hasCompatibleFilterTypes,
    focusValue(position) {
      const ref = `filter-value-${position}`
      if (
        position >= 0 &&
        Object.prototype.hasOwnProperty.call(this.$refs, ref) &&
        this.$refs[ref][0] &&
        Object.prototype.hasOwnProperty.call(this.$refs[ref][0], 'focus')
      ) {
        this.$refs[ref][0].focus()
      }
    },
    /**
     * Returns a list of filter types that are allowed for the given fieldId.
     */
    allowedFilters(filterTypes, fields, fieldId) {
      const field = fields.find((f) => f.id === fieldId)
      return Object.values(filterTypes).filter((filterType) => {
        return field !== undefined && filterType.fieldIsCompatible(field)
      })
    },
    deleteFilter(event, filter) {
      event.deletedFilterEvent = true
      const groupNode = this.filtersTree.findGroup(filter.filter_group)
      const lastInGroup = groupNode && groupNode.filters.length === 1
      if (lastInGroup) {
        groupNode.remove()
        this.$emit('deleteFilterGroup', groupNode.group)
      } else {
        this.$emit('deleteFilter', filter)
      }
    },
    /**
     * Updates a filter with the given values. Some data manipulation will also be done
     * because some filter types are not compatible with certain field types.
     */
    updateFilter(filter, values) {
      const fieldId = Object.prototype.hasOwnProperty.call(values, 'field')
        ? values.field
        : filter.field
      const type = Object.prototype.hasOwnProperty.call(values, 'type')
        ? values.type
        : filter.type
      const value = Object.prototype.hasOwnProperty.call(values, 'value')
        ? values.value
        : filter.value

      // If the field has changed we need to check if the filter type is compatible
      // and if not we are going to choose the first compatible type.
      if (Object.prototype.hasOwnProperty.call(values, 'field')) {
        const allowedFilterTypes = this.allowedFilters(
          this.filterTypes,
          this.fields,
          fieldId
        ).map((filter) => filter.type)
        if (!allowedFilterTypes.includes(type)) {
          values.type = allowedFilterTypes[0]
        }
      }

      // If the type or value has changed it could be that the value needs to be
      // formatted or prepared.
      if (
        Object.prototype.hasOwnProperty.call(values, 'field') ||
        Object.prototype.hasOwnProperty.call(values, 'type') ||
        Object.prototype.hasOwnProperty.call(values, 'value')
      ) {
        const filterType = this.$registry.get('viewFilter', type)
        const field = this.fields.find(({ id }) => id === fieldId)
        values.value = filterType.prepareValue(value, field, true)
      }

      this.$emit('updateFilter', { filter, values })
    },
    /**
     * Returns the input component related to the filter type. This component is
     * responsible for updating the filter value.
     */
    getInputComponent(type, fieldId) {
      const field = this.fields.find(({ id }) => id === fieldId)
      return this.$registry.get('viewFilter', type).getInputComponent(field)
    },
    fieldIdExists(fields, fieldId) {
      return fields.findIndex((field) => field.id === fieldId) !== -1
    },
    fieldIsCompatible(filterType, fieldId) {
      const field = this.fields.find(({ id }) => id === fieldId)
      return this.$registry
        .get('viewFilter', filterType)
        .fieldIsCompatible(field)
    },
    getFirstCompatibleField(fields) {
      return fields
        .slice()
        .sort((a, b) => b.primary - a.primary)
        .find((field) => hasCompatibleFilterTypes(field, this.filterTypes))
    },
  },
}
</script>
