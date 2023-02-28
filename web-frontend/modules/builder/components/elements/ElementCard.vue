<template>
  <div class="element-card">
    <div>
      <i :class="`fas fa-${elementType.iconClass}`"></i>
      <span class="margin-left-1">{{ elementType.name }}</span>
    </div>
    <div class="margin-top-1 element-card__description">
      {{ elementType.description }}
    </div>
  </div>
</template>

<script>
export default {
  name: 'ElementCard',
  props: {
    elementType: {
      type: Object,
      required: true,
    },
  },
}
</script>
