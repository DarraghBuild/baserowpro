<template>
  <div>{{ element }}</div>
</template>

<script>
export default {
  name: 'Element',
  props: {
    element: {
      type: Object,
      required: true,
    },
  },
}
</script>
