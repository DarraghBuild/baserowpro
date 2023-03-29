<template>
  <div>
    <a
      ref="contextLink"
      class="header__filter-link"
      :class="{
        active: view.filters.length > 0,
      }"
      @click="$refs.context.toggle($refs.contextLink, 'bottom', 'left', 4)"
    >
      <i class="header__filter-icon fas fa-filter"></i>
      <span class="header__filter-name">{{
        $tc('viewFilter.filter', view.filters.length, {
          count: view.filters.length,
        })
      }}</span>
    </a>
    <Context
      ref="context"
      class="filters"
      :overflow-y="contextOverflowY"
      :class="{ 'context--loading-overlay': view._.loading }"
    >
      <ViewFilterForm
        class="filters_main"
        :fields="fields"
        :view="view"
        :read-only="readOnly"
        :disable-filter="disableFilter"
        :dropdown-target="dropdownTarget"
        @changed="$emit('changed')"
        @dropdown-open="$refs.context.toggleScroll()"
        @dropdown-closed="$refs.context.toggleScroll()"
      />

      <template #footer>
        <div v-if="!disableFilter" class="filters_footer">
          <a class="filters__add" @click.prevent="addFilter()">
            <i class="fas fa-plus"></i>
            {{ $t('viewFilterContext.addFilter') }}</a
          >
          <div v-if="view.filters.length > 0">
            <SwitchInput
              :value="view.filters_disabled"
              @input="updateView(view, { filters_disabled: $event })"
              >{{ $t('viewFilterContext.disableAllFilters') }}</SwitchInput
            >
          </div>
        </div>
      </template>
    </Context>
  </div>
</template>

<script>
import ViewFilterForm from '@baserow/modules/database/components/view/ViewFilterForm'
import { notifyIf } from '@baserow/modules/core/utils/error'
import { hasCompatibleFilterTypes } from '@baserow/modules/database/utils/field'

export default {
  name: 'ViewFilter',
  components: { ViewFilterForm },
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
  },
  data() {
    return {
      contextOverflowY: 'auto',
      dropdownTarget: null,
    }
  },
  computed: {
    filterTypes() {
      return this.$registry.getAll('viewFilter')
    },
  },
  mounted() {
    this.dropdownTarget = {
      HTMLElement: this.$refs.context.getContainerElement(),
    }
  },
  beforeMount() {
    this.$bus.$on('view-filter-created', this.filterCreated)
  },
  beforeDestroy() {
    this.$bus.$off('view-filter-created', this.filterCreated)
  },
  methods: {
    /**
     * When a filter is created via an outside source we want to show the context menu.
     */
    filterCreated() {
      this.$refs.context.show(this.$refs.contextLink, 'bottom', 'left', 4)
    },
    async addFilter(values) {
      try {
        const field = this.getFirstCompatibleField(this.fields)
        if (field === undefined) {
          await this.$store.dispatch('toast/error', {
            title: this.$t(
              'viewFilterContext.noCompatibleFilterTypesErrorTitle'
            ),
            message: this.$t(
              'viewFilterContext.noCompatibleFilterTypesErrorMessage'
            ),
          })
        } else {
          await this.$store.dispatch('view/createFilter', {
            field,
            view: this.view,
            values: {
              field: field.id,
            },
            emitEvent: false,
            readOnly: this.readOnly,
          })
          this.$emit('changed')
        }
      } catch (error) {
        notifyIf(error, 'view')
      }
    },
    /**
     * Updates the view filter type. It will mark the view as loading because that
     * will also trigger the loading state of the second filter.
     */
    async updateView(view, values) {
      this.$store.dispatch('view/setItemLoading', { view, value: true })

      try {
        await this.$store.dispatch('view/update', {
          view,
          values,
          readOnly: this.readOnly,
        })
        this.$emit('changed')
      } catch (error) {
        notifyIf(error, 'view')
      }

      this.$store.dispatch('view/setItemLoading', { view, value: false })
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
