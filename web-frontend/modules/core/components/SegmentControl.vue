<template>
  <div class="segment-control">
    <button
      v-for="(segment, index) in segments"
      :key="index"
      :class="{ 'segment-control__button--active': index === activeIndex }"
      class="segment-control__button"
      @click="setActiveIndex(index)"
    >
      {{ segment }}
    </button>
  </div>
</template>

<script>
export default {
  name: 'SegmentControl',
  props: {
    /**
     * The segments to display.
     */
    segments: {
      type: Array,
      required: true,
      default: () => [],
    },
    /**
     * The index of the active segment.
     */
    initialActiveIndex: {
      type: Number,
      required: false,
      default: 0,
    },
  },
  data() {
    return {
      activeIndex: this.initialActiveIndex,
    }
  },
  methods: {
    setActiveIndex(index) {
      this.activeIndex = index
      this.$emit('update:activeIndex', index)
    },
  },
}
</script>
