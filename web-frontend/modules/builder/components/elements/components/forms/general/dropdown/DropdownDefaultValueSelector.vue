<template>
  <FormElement class="control">
    <label class="control__label">{{ $t('generalForm.valueTitle') }}</label>
    <Dropdown
      :value="value"
      :show-search="false"
      @input="$emit('input', $event)"
    >
      <DropdownItem
        v-for="option in options"
        :key="option.id"
        :name="resolveFormula(option.name)"
        :value="option.id"
      ></DropdownItem>
    </Dropdown>
  </FormElement>
</template>

<script>
import ResolveFormulaMixin from '@baserow/modules/builder/mixins/resolveFormula'

export default {
  name: 'DropdownDefaultValueSelector',
  mixins: [ResolveFormulaMixin],
  props: {
    value: {
      type: Number,
      required: false,
      default: null,
    },
    options: {
      type: Array,
      required: false,
      default: () => [],
    },
  },
  computed: {
    applicationContext() {
      return {
        builder: this.builder,
        page: this.page,
        mode: this.mode,
        element: this.element,
      }
    },
  },
}
</script>
