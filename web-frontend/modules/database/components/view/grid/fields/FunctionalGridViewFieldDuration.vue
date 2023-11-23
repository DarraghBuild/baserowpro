<template functional>
  <div ref="cell" class="grid-view__cell" :class="data.staticClass || ''">
    <div v-if="props.value" class="grid-field-duration">{{ props.value }}</div>
    <div v-else class="grid-field-duration-placeholder">
      {{ props.field.duration_format }}
    </div>
  </div>
</template>
