<template>
  <div class="row">
    <div class="col col-5">
      <input
        type="text"
        class="input"
        :value="option.value"
        @input="$emit('update', { value: $event.target.value })"
      />
    </div>
    <div class="col col-5">
      <input
        type="text"
        class="input"
        :value="option.name"
        @input="$emit('update', { name: $event.target.value })"
      />
    </div>
    <div class="dropdown-option__delete col col-1">
      <Button
        tag="a"
        icon="iconoir-trash"
        type="ghost"
        @click="$emit('delete')"
      ></Button>
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
