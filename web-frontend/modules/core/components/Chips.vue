<template>
  <button class="chips" :class="{ 'chips--active': active }" v-on="$listeners">
    <slot />
  </button>
</template>

<script>
export default {
  name: 'Chips',
  props: {
    active: {
      type: Boolean,
      default: false,
    },
  },
}
</script>
