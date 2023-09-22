<template>
  <div>
    <div>
      <div
        v-for="color in options.colors || []"
        :key="color.id"
        v-sortable="{
          id: color.id,
          update: orderColor,
          handle: '[data-sortable-handle]',
          marginTop: -5,
        }"
        class="conditional-color-value-provider-form__color"
      >
        <div class="conditional-color-value-provider-form__color-header">
          <div
            class="conditional-color-value-provider-form__color-handle"
            data-sortable-handle
          ></div>
          <a
            :ref="`colorSelect-${color.id}`"
            class="conditional-color-value-provider-form__color-color"
            :class="`background-color--${color.color}`"
            @click="openColor(color)"
          >
            <i class="iconoir-nav-arrow-down"></i>
          </a>
          <div :style="{ flex: 1 }" ></div>
          <a
            v-if="options.colors.length > 1"
            class="conditional-color-value-provider-form__color-trash-link"
            @click="deleteColor(color)"
          >
            <i class="iconoir-bin" />
          </a>
        </div>
        <div
          v-if="color.filters.length === 0"
          class="conditional-color-value-provider-form__color-filter--empty"
        >
          {{ $t('conditionalColorValueProviderForm.colorAlwaysApply') }}
        </div>
        <ViewFieldConditionsForm
          v-show="color.filters.length !== 0"
          class="conditional-color-value-provider-form__color-filters"
          :filters="color.filters"
          :filterGroups="color.filter_groups"
          :disable-filter="false"
          :filter-type="color.operator"
          :fields="fields"
          :view="view"
          :read-only="readOnly"
          @addFilter="addFilter(color, $event)"
          @deleteFilter="deleteFilter(color, $event)"
          @updateFilter="updateFilter(color, $event)"
          @selectOperator="updateColor(color, { operator: $event })"
          @deleteFilterGroup="deleteFilterGroup(color, $event)"
          @selectFilterGroupOperator="updateFilterGroupOperator(color, $event)"
        />
        <a
          class="conditional-color-value-provider-form__color-filter-add"
          @click.prevent="addFilter(color)"
        >
          <i class="iconoir-plus"></i>
          {{ $t('conditionalColorValueProviderForm.addCondition') }}
        </a>
        <a
          class="conditional-color-value-provider-form__color-filter-add"
          @click.prevent="addFilterGroup(color)"
        >
          <i class="iconoir-plus"></i>
          {{ $t('conditionalColorValueProviderForm.addConditionGroup') }}
        </a>
        <ColorSelectContext
          :ref="`colorContext-${color.id}`"
          @selected="updateColor(color, { color: $event })"
        ></ColorSelectContext>
      </div>
    </div>
    <a class="colors__add" @click.prevent="addColor()">
      <i class="iconoir-plus"></i>
      {{ $t('conditionalColorValueProviderForm.addColor') }}</a
    >
  </div>
</template>

<script>
import ViewFieldConditionsForm from '@baserow/modules/database/components/view/ViewFieldConditionsForm'
import ColorSelectContext from '@baserow/modules/core/components/ColorSelectContext'
import { ConditionalColorValueProviderType } from '@baserow_premium/decoratorValueProviders'

export default {
  name: 'ConditionalColorValueProvider',
  components: { ViewFieldConditionsForm, ColorSelectContext },
  props: {
    options: {
      type: Object,
      required: true,
    },
    view: {
      type: Object,
      required: true,
    },
    table: {
      type: Object,
      required: true,
    },
    fields: {
      type: Array,
      required: true,
    },
    readOnly: {
      type: Boolean,
      required: true,
    },
  },
  methods: {
    orderColor(colorIds) {
      const newColors = colorIds.map((colorId) =>
        this.options.colors.find(({ id }) => id === colorId)
      )
      this.$emit('update', {
        colors: newColors,
      })
    },
    openColor(color) {
      this.$refs[`colorContext-${color.id}`][0].setActive(color.color)
      this.$refs[`colorContext-${color.id}`][0].toggle(
        this.$refs[`colorSelect-${color.id}`][0],
        'bottom',
        'left',
        4
      )
    },
    addColor() {
      const colorToExclude = this.options.colors.map((color) => color.color)
      this.$emit('update', {
        colors: [
          ...this.options.colors,
          ConditionalColorValueProviderType.getDefaultColorConf(
            this.$registry,
            {
              fields: this.fields,
            },
            true,
            colorToExclude
          ),
        ],
      })
    },
    updateColor(color, values) {
      const newColors = this.options.colors.map((colorConf) => {
        if (colorConf.id === color.id) {
          return { ...colorConf, ...values }
        }
        return colorConf
      })

      this.$emit('update', {
        colors: newColors,
      })
    },
    deleteColor(color) {
      const newColors = this.options.colors.filter(({ id }) => {
        return id !== color.id
      })

      this.$emit('update', {
        colors: newColors,
      })
    },
    addFilterGroup(color) {
      const filterGroup = ConditionalColorValueProviderType.getDefaultFilterGroupConf()
      const newColors = this.options.colors.map((colorConf) => {
        if (colorConf.id === color.id) {
          return {
            ...colorConf,
            filter_groups: [...(colorConf.filter_groups || []), filterGroup],
            filters: [
              ...colorConf.filters,
              ConditionalColorValueProviderType.getDefaultFilterConf(
                this.$registry,
                {
                  fields: this.fields,
                  filterGroupId: filterGroup.id,
                }
              ),
            ],
          }
        }
        return colorConf
      })

      this.$emit('update', {
        colors: newColors,
      })
    },
    updateFilterGroupOperator(color, { value, filterGroup }) {
      const newColors = this.options.colors.map((colorConf) => {
        if (colorConf.id === color.id) {
          const newFilterGroups = colorConf.filter_groups.map((group) => {
            if (group.id === filterGroup.id) {
              return { ...group, filter_type: value }
            }
            return group
          })
          return {
            ...colorConf,
            filter_groups: newFilterGroups,
          }
        }
        return colorConf
      })

      this.$emit('update', {
        colors: newColors,
      })
    },
    addFilter(color, filterGroupId = null) {
      const newColors = this.options.colors.map((colorConf) => {
        if (colorConf.id === color.id) {
          return {
            ...colorConf,
            filters: [
              ...colorConf.filters,
              ConditionalColorValueProviderType.getDefaultFilterConf(
                this.$registry,
                {
                  fields: this.fields,
                  filterGroupId,
                }
              ),
            ],
          }
        }
        return colorConf
      })

      this.$emit('update', {
        colors: newColors,
      })
    },
    updateFilter(color, { filter, values }) {
      const newColors = this.options.colors.map((colorConf) => {
        if (colorConf.id === color.id) {
          const newFilters = colorConf.filters.map((filterConf) => {
            if (filterConf.id === filter.id) {
              return { ...filter, ...values }
            }
            return filterConf
          })
          return {
            ...colorConf,
            filters: newFilters,
          }
        }
        return colorConf
      })

      this.$emit('update', {
        colors: newColors,
      })
    },
    deleteFilter(color, filter) {
      const newColors = this.options.colors.map((colorConf) => {
        if (colorConf.id === color.id) {
          const newFilters = colorConf.filters.filter((filterConf) => {
            return filterConf.id !== filter.id
          })
          return {
            ...colorConf,
            filters: newFilters,
          }
        }
        return colorConf
      })

      this.$emit('update', {
        colors: newColors,
      })
    },
    deleteFilterGroup(color, filterGroup) {
      const newColors = this.options.colors.map((colorConf) => {
        if (colorConf.id === color.id) {
          const newFilters = colorConf.filters.filter((filterConf) => {
            return filterConf.filter_group !== filterGroup.id
          })
          const newFilterGroups = colorConf.filter_groups.filter((group) => {
            return group.id !== filterGroup.id
          })
          return {
            ...colorConf,
            filters: newFilters,
            filter_groups: newFilterGroups,
          }
        }
        return colorConf
      })

      this.$emit('update', {
        colors: newColors,
      })
    },
  },
}
</script>
