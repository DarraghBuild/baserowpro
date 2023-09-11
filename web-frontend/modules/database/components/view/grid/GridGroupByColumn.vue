<template>
  <div
    class="grid-group-by__column"
    :class="{
      'grid-group-by__column-header-bottom': isFooter,
    }"
  >
    <div v-if="isHeader" class="grid-group-by__column-name">
      {{ groupByFieldName }}
    </div>
    <a v-if="isHeader" class="grid-group-by__collapse" @click="toggleCollapsed"
      ><i class="fas" :class="!collapsed ? 'fa-minus' : 'fa-plus'"></i>
    </a>

    <div v-if="isHeader" class="grid-group-by__column-value-wrapper">
      <component
        :is="functionalComponent"
        :workspace-id="workspaceId"
        :field="groupByField"
        :value="groupByValue"
        :state="state"
        :read-only="true"
      />
    </div>

    <div v-if="isHeader && groupByCount" class="grid-group-by__count">
      {{ groupByCount }}
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'GridGroupByColumn',
  props: {
    groupBy: {
      type: Object,
      required: true,
    },
    row: {
      type: Object,
      required: true,
    },
    view: {
      type: Object,
      required: true,
    },
    storePrefix: {
      type: String,
      required: true,
    },
    allFields: {
      type: Array,
      required: true,
    },
    workspaceId: {
      type: Number,
      required: true,
    },
    isHeader: {
      type: Boolean,
      required: true,
    },
    isFooter: {
      type: Boolean,
      required: true,
    },
    levelGroupInfo: {
      type: Array,
      required: true,
    },
    parentGroupBys: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      state: {},
    }
  },
  computed: {
    groupByField() {
      return this.allFields.find((f) => f.id === this.groupBy.field)
    },
    groupByCount() {
      const groupInfo = this.levelGroupInfo?.find(this.keyMatches)
      return groupInfo ? groupInfo?.aggregations?.count : null
    },
    groupByFieldName() {
      return this.groupByField.name
    },
    groupByValue() {
      return this.row[`field_${this.groupBy.field}`]
    },
    functionalComponent() {
      return this.$registry
        .get('field', this.groupByField.type)
        .getFunctionalGridViewFieldComponent()
    },
    fullGroupKey() {
      return JSON.stringify(Object.values(this.groupKeyMap))
    },
    groupKeyMap() {
      const keyPath = [...this.parentGroupBys, this.groupBy]
      const o = new Map()
      for (let i = 0; i < keyPath.length; i++) {
        const gb = keyPath[i]
        const fieldName = `field_${gb.field}`
        const value = this.row[fieldName]
        o[fieldName] = value
      }
      return o
    },
    collapsed() {
      const keyPath = [...this.parentGroupBys, this.groupBy]
      const pathSoFar = []
      let lowestSetValue = false
      for (let i = 0; i < keyPath.length; i++) {
        const gb = keyPath[i]
        const fieldName = `field_${gb.field}`
        const value = this.row[fieldName]
        pathSoFar.push(value)
        const result = this.getGroupCollapsed(JSON.stringify(pathSoFar))
        if (result != null) {
          lowestSetValue = result
        }
      }
      return lowestSetValue
    },
  },
  beforeCreate() {
    this.$options.computed = {
      ...(this.$options.computed || {}),
      ...mapGetters({
        getGroupCollapsed:
          this.$options.propsData.storePrefix + 'view/grid/getGroupCollapsed',
      }),
    }
  },
  methods: {
    keyMatches(groupBy) {
      const keyPath = [...this.parentGroupBys, this.groupBy]
      for (let i = 0; i < keyPath.length; i++) {
        const gb = keyPath[i]
        const fieldName = `field_${gb.field}`
        const value = this.row[fieldName]
        const field = this.allFields.find((f) => f.id === gb.field)
        if (!this.compareKeys(value, groupBy.key[fieldName], field)) {
          return false
        }
      }
      return true
    },
    compareKeys(rowValue, groupLevelValue, field) {
      if (field.type === 'single_select') {
        return rowValue
          ? rowValue.id === groupLevelValue
          : rowValue === groupLevelValue
      } else {
        return JSON.stringify(rowValue) === JSON.stringify(groupLevelValue)
      }
    },
    toggleCollapsed() {
      this.$store.dispatch(this.storePrefix + 'view/grid/setGroupCollapsed', {
        groupKey: this.fullGroupKey,
        collapsed: !this.collapsed,
        view: this.view,
        fields: this.allFields,
      })
    },
  },
}
</script>
