<template>
  <div class="row">
    <div class="col col-6">
      <input
        type="text"
        class="input"
        :value="option.value"
        @input="$emit('update', { value: $event.target.value })"
      />
    </div>
    <div class="col col-6">
      <input
        type="text"
        class="input"
        :value="option.name"
        @input="$emit('update', { name: $event.target.value })"
      />
    </div>
  </div>
</template>

<script>
export default {
  name: 'DropdownOption',
  props: {
    option: {
      type: Object,
      required: true,
    },
  },
}
</script>
