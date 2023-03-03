<template>
  <div class="element__menu">
    <a class="element__menu-item">
      <i class="fas fa-copy"></i>
      <div class="element__menu-item-description">
        {{ $t('action.copy') }}
      </div>
    </a>
    <a
      class="element__menu-item"
      :class="{ disabled: moveUpDisabled }"
      @click="!moveUpDisabled && $emit('move', 'up')"
    >
      <i class="fas fa-arrow-up"></i>
      <div class="element__menu-item-description">
        {{ $t('elementMenu.moveUp') }}
      </div>
    </a>
    <a
      class="element__menu-item"
      :class="{ disabled: moveDownDisabled }"
      @click="!moveDownDisabled && $emit('move', 'down')"
    >
      <i class="fas fa-arrow-down"></i>
      <div class="element__menu-item-description">
        {{ $t('elementMenu.moveDown') }}
      </div>
    </a>
    <a class="element__menu-item" @click="$emit('delete')">
      <i class="fas fa-trash"></i>
      <div class="element__menu-item-description">
        {{ $t('action.delete') }}
      </div>
    </a>
  </div>
</template>

<script>
export default {
  name: 'ElementMenu',
  props: {
    moveUpDisabled: {
      type: Boolean,
      required: false,
      default: false,
    },
    moveDownDisabled: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
}
</script>
