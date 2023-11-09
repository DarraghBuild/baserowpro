<template>
  <div class="paginator">
    <!-- <div class="paginator__name"></div> -->

    <a
      class="paginator__button"
      :class="{
        'paginator__button--disabled': page === 1,
      }"
      @click="changePage(page - 1)"
    >
      <i class="iconoir-nav-arrow-left"></i>
    </a>

    <div class="paginator__content">
      <span class="paginator__content-text">{{ $t('paginator.page') }}</span>
      <span class="paginator__content-current-page">{{ page }}</span>
      <span>{{ $t('paginator.of', { pages: totalPages }) }}</span>
    </div>

    <a
      class="paginator__button"
      :class="{
        'paginator__button--disabled': page === totalPages,
      }"
      @click="changePage(page + 1)"
    >
      <i class="iconoir-nav-arrow-right"></i>
    </a>
  </div>
</template>
<script>
export default {
  name: 'Paginator',
  props: {
    /**
     * The total number of pages available.
     */
    totalPages: {
      required: true,
      type: Number,
      default: 0,
      validator: (prop) => typeof prop === 'number' || prop === null,
    },
    /**
     * The currently selected page.
     */
    page: {
      required: true,
      type: Number,
      default: 0,
    },
  },
  watch: {
    page(newPage) {
      this.textInputPage = newPage
    },
  },
  methods: {
    changePage(newPage) {
      if (newPage <= this.totalPages && newPage > 0)
        this.$emit('change-page', newPage)
    },
  },
}
</script>
