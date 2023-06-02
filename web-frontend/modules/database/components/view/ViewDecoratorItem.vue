<template functional>
  <div class="decorator-item">
    <img class="decorator-item__image" :src="props.decoratorType.getImage()" />
    <div class="decorator-item__content">
      <div class="decorator-item__title">
        <span class="decorator-item__title-title">{{
          props.decoratorType.getName()
        }}</span>
        <span v-if="props.deactivated" class="deactivated-label">
          <i class="iconoir-lock"></i>
        </span>
      </div>
      <div class="decorator-item__description">
        {{ props.decoratorType.getDescription() }}
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ViewDecoratorItem',
  props: {
    decoratorType: {
      type: Object,
      required: true,
    },
    deactivated: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
}
</script>
