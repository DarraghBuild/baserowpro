<template functional>
  <li
    class="select__item"
    :class="{
      hidden: !$options.methods.isVisible(parent),
      active: $options.methods.isActive(props.value, parent),
      disabled: props.disabled,
      hover: $options.methods.isHovering(props.value, parent),
    }"
  >
    <a
      class="select__item-link"
      @click="$options.methods.select(props.value, props.disabled)"
      @mousemove="$options.methods.hover(props.value, props.disabled)"
    >
      <div class="select__item-name">
        <slot>
          <i
            v-if="props.icon"
            v-tooltip="props.iconTooltip"
            class="select__item-icon fas fa-fw"
            :class="'fa-' + props.icon"
          />
          <img
            v-if="props.image"
            class="select__item-image"
            :src="props.image"
          />
          <span class="select__item-name-text" :title="props.name">{{
            props.name
          }}</span>
        </slot>
      </div>
      <div v-if="props.description !== null" class="select__item-description">
        {{ props.description }}
      </div>
    </a>
  </li>
</template>

<script>
import dropdownItem from '@baserow/modules/core/mixins/dropdownItem'

export default {
  name: 'DropdownItem',
  mixins: [dropdownItem],
}
</script>
