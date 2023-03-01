<template>
  <ul>
    <li v-for="element in elements" :key="element.type">
      <ElementsListItem :element="element" />
    </li>
  </ul>
</template>

<script>
import ElementsListItem from '@baserow/modules/builder/components/elements/ElementsListItem'
export default {
  name: 'ElementsList',
  components: { ElementsListItem },
  props: {
    elements: {
      type: Array,
      required: true,
    },
  },
}
</script>
