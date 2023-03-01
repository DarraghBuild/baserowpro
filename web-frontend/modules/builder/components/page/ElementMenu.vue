<template>
  <div class="element__menu">
    <a class="element__menu-item">
      <i class="fas fa-copy"></i>
      <div class="element__menu-item-description">
        {{ $t('action.copy') }}
      </div>
    </a>
    <a class="element__menu-item">
      <i class="fas fa-arrow-up"></i>
      <div class="element__menu-item-description">
        {{ $t('elementMenu.moveUp') }}
      </div>
    </a>
    <a class="element__menu-item">
      <i class="fas fa-arrow-down"></i>
      <div class="element__menu-item-description">
        {{ $t('elementMenu.moveDown') }}
      </div>
    </a>
    <a class="element__menu-item">
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
}
</script>
