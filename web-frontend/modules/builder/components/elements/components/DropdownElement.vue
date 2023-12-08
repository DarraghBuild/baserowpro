<template>
  <div class="control">
    <label v-if="element.label" class="control__label">
      {{ resolveFormula(element.label) }}
    </label>
    <Dropdown
      v-model="itemSelected"
      :placeholder="resolveFormula(element.placeholder)"
      :show-search="false"
      :disabled="mode === 'editing'"
    >
      <DropdownItem
        v-for="option in element.options"
        :key="option.id"
        :name="resolveFormula(option.name)"
        :value="option.value"
      ></DropdownItem>
    </Dropdown>
  </div>
</template>

<script>
import formElement from '@baserow/modules/builder/mixins/formElement'

export default {
  name: 'DropdownElement',
  mixins: [formElement],
  props: {
    /**
     * @type {Object}
     * @property {string} label - The label displayed above the dropdown
     * @property {number} default_value - The default value selected
     * @property {string} placeholder - The placeholder value of the dropdown
     * @property {boolean} required - If the element is required for form submission
     * @property {Array} options - The options of the dropdown
     */
    element: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      itemSelected: null,
    }
  },
  watch: {
    itemSelected(value) {
      this.setFormData(this.resolveFormula(value))
    },
    'element.default_value': {
      handler() {
        this.setItemSelected()
      },
      immediate: true,
    },
    'element.options': {
      handler() {
        this.setItemSelected()
      },
      deep: true,
    },
  },
  methods: {
    setItemSelected() {
      this.itemSelected = this.element.options.find(
        (option) => option.id === this.element.default_value
      )?.value
    },
  },
}
</script>
