<template>
  <div class="grid-group-by__cells">
    <GridGroupByColumn
      v-for="(d, level) in groupBys"
      :key="d.groupBy.field"
      :view="view"
      :group-by="d.groupBy"
      :store-prefix="storePrefix"
      :all-fields="allFields"
      :workspace-id="workspaceId"
      :is-header="d.isHeader"
      :is-footer="d.isFooter"
      :row="row"
      :level-group-info="getGroupInfo(level)"
      :parent-group-bys="groupBys.slice(0, level).map((g) => g.groupBy)"
    ></GridGroupByColumn>
  </div>
</template>

<script>
import GridGroupByColumn from '@baserow/modules/database/components/view/grid/GridGroupByColumn.vue'
import { mapGetters } from 'vuex'

export default {
  name: 'GridGroupByCells',
  components: {
    GridGroupByColumn,
  },
  props: {
    view: {
      type: Object,
      required: true,
    },
    row: {
      type: Object,
      required: true,
    },
    previousRow: {
      type: Object,
      required: false,
      default: () => undefined,
    },
    nextRow: {
      type: Object,
      required: false,
      default: () => undefined,
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
    isVeryFirstRow: {
      type: Boolean,
      required: true,
    },
  },
  data() {
    return {
      state: {},
    }
  },

  computed: {
    groupBys() {
      const groupByData = []
      let isHeader = false
      let isFooter = false
      for (const groupBy of this.view.group_bys) {
        const value = this.row[`field_${groupBy.field}`]
        if (!isHeader) {
          if (this.previousRow) {
            const prevValue = this.previousRow[`field_${groupBy.field}`]
            isHeader =
              prevValue === undefined || !this.compareValues(prevValue, value)
          } else if (
            this.isVeryFirstRow &&
            this.isRowVeryFirstRow(this.row.id)
          ) {
            isHeader = true
          }
        }
        if (!isFooter) {
          const nextValue = this.nextRow
            ? this.nextRow[`field_${groupBy.field}`]
            : undefined
          isFooter =
            nextValue === undefined || !this.compareValues(nextValue, value)
        }
        groupByData.push({ groupBy, isHeader, isFooter })
      }
      return groupByData
    },
  },
  beforeCreate() {
    this.$options.computed = {
      ...(this.$options.computed || {}),
      ...mapGetters({
        isRowVeryFirstRow:
          this.$options.propsData.storePrefix + 'view/grid/isRowVeryFirstRow',
        getGroupInfo:
          this.$options.propsData.storePrefix + 'view/grid/getGroupInfo',
      }),
    }
  },
  methods: {
    compareValues(a, b) {
      return JSON.stringify(a) === JSON.stringify(b)
    },
  },
}
</script>
