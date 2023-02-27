<template>
  <a class="add-element-button" @click="$emit('click')">
    <div>
      <i class="fas fa-stream"></i>
      <span class="margin-left-1">{{ $t('addElementButton.label') }}</span>
    </div>
    <i class="fas fa-plus"></i>
  </a>
</template>

<script>
export default {
  name: 'AddElementButton',
}
</script>
