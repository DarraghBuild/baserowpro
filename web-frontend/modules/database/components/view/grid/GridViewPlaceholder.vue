<template>
  <div
    class="grid-view__placeholder"
    :style="{
      width: placeholderWidth + 'px',
    }"
  >
    <div
      v-for="height in placeholderHeights"
      :style="{
        height: height + 'px',
        width: placeholderWidth + 'px',
      }"
    >
      <div
        v-for="(value, index) in placeholderPositions"
        :key="'placeholder-column-' + index"
        class="grid-view__placeholder-column"
        :style="{ left: value - 1 + 'px' }"
      ></div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

import gridViewHelpers from '@baserow/modules/database/mixins/gridViewHelpers'

export default {
  name: 'GridViewPlaceholder',
  mixins: [gridViewHelpers],
  props: {
    fields: {
      type: Array,
      required: true,
    },
    includeRowDetails: {
      type: Boolean,
      required: true,
    },
  },
  computed: {
    /**
     * Calculate the left positions of the placeholder columns. These are the gray
     * vertical lines that are always visible, even when the data hasn't loaded yet.
     */
    placeholderPositions() {
      let last = 0
      const placeholderPositions = {}
      this.fields.forEach((field) => {
        last += this.getFieldWidth(field.id)
        placeholderPositions[field.id] = last
      })
      return placeholderPositions
    },
    placeholderHeights() {
      let number = this.placeholderHeight
      const result = []
      while (number > 0) {
        const chunk = Math.min(number, this.maxPlaceholderHeight)
        result.push(chunk)
        number -= chunk
      }
      return result
    },
    placeholderWidth() {
      let width = this.fields.reduce(
        (value, field) => this.getFieldWidth(field.id) + value,
        0
      )
      if (this.includeRowDetails) {
        width += this.gridViewRowDetailsWidth
      }
      return width
    },
    maxPlaceholderHeight() {
      return Math.pow(2, 20)
    },
  },
  beforeCreate() {
    this.$options.computed = {
      ...(this.$options.computed || {}),
      ...mapGetters({
        placeholderHeight:
          this.$options.propsData.storePrefix +
          'view/grid/getPlaceholderHeight',
      }),
    }
  },
}
</script>
