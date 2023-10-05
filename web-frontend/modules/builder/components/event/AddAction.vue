<template>
  <div class="add-action">
    <a
      v-if="!loading"
      class="anchor add-action__button"
      @click="$emit('click')"
    >
      <i class="iconoir-plus margin-right-1"></i>
      {{ $t('addAction.caption') }}
    </a>
    <div v-else class="loading"></div>
  </div>
</template>

<script>
export default {
  name: 'AddAction',
  props: {
    loading: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
}
</script>
