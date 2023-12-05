<template>
  <div>
    <label v-if="element.label" class="control__label">
      {{ resolveFormula(element.label) }}
    </label>
    <input
      type="text"
      class="input-element"
      :readonly="isEditable"
      :value="resolveFormula(element.default_value)"
      :required="element.required"
      :placeholder="resolveFormula(element.placeholder)"
      @input="setFormData($event.target.value)"
    />
  </div>
</template>

<script>
import formElement from '@baserow/modules/builder/mixins/formElement'

export default {
  name: 'InputTextElement',
  mixins: [formElement],
  props: {
    /**
     * @type {Object}
     * @property {string} default_value - The text input's default value.
     * @property {boolean} required - Whether the text input is required.
     * @property {Object} placeholder - The text input's placeholder value.
     */
    element: {
      type: Object,
      required: true,
    },
  },
  watch: {
    'element.default_value'(value) {
      this.setFormData(this.resolveFormula(value))
    },
  },
}
</script>
