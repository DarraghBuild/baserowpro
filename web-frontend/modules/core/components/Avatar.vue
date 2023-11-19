<template>
  <div
    class="avatar"
    :class="{
      'avatar--rounded': rounded,
      [`avatar--${size}`]: true,
      [`avatar--${color}`]: color,
    }"
  >
    <!-- <i v-if="icon" class="fas" :class="`fa-${icon}`" /> -->
    <img v-if="image" :src="image" class="avatar__image" />
    <span v-if="initials && !image" class="avatar__initials">{{
      initials
    }}</span>
  </div>
</template>

<script>
export default {
  name: 'Avatar',
  props: {
    /**
     * The URL of the image to display.
     */
    image: {
      type: String,
      required: false,
      default: null,
    },
    /**
     * If true the avatar will be rounded.
     */
    rounded: {
      type: Boolean,
      required: false,
      default: false,
    },
    /**
     * The initials to display if no image is provided
     */
    initials: {
      type: String,
      required: false,
      default: null,
    },
    /**
     * The background color of the avatar
     */
    color: {
      required: false,
      type: String,
      default: 'blue',
      validator: function (value) {
        return [
          'blue',
          'cyan',
          'green',
          'yellow',
          'red',
          'magenta',
          'purple',
          'neutral',
        ].includes(value)
      },
    },
    /**
     * The size of the avatar
     */
    size: {
      type: String,
      required: false,
      default: 'medium',
      validator: function (value) {
        return ['small', 'medium', 'large', 'x-large'].includes(value)
      },
    },
  },
}
</script>
