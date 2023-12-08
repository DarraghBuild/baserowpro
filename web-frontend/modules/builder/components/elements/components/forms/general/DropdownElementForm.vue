<template>
  <form @submit.prevent @keydown.enter.prevent>
    <ApplicationBuilderFormulaInputGroup
      v-model="values.label"
      :label="$t('generalForm.labelTitle')"
      :placeholder="$t('generalForm.labelPlaceholder')"
      :data-providers-allowed="DATA_PROVIDERS_ALLOWED_FORM_ELEMENTS"
    ></ApplicationBuilderFormulaInputGroup>
    <DropdownDefaultValueSelector
      v-model="values.default_value"
      :options="values.options"
    ></DropdownDefaultValueSelector>
    <ApplicationBuilderFormulaInputGroup
      v-model="values.placeholder"
      :label="$t('generalForm.placeholderTitle')"
      :placeholder="$t('generalForm.placeholderPlaceholder')"
      :data-providers-allowed="DATA_PROVIDERS_ALLOWED_FORM_ELEMENTS"
    ></ApplicationBuilderFormulaInputGroup>
    <FormElement class="control">
      <label class="control__label">
        {{ $t('generalForm.requiredTitle') }}
      </label>
      <div class="control__elements">
        <Checkbox v-model="values.required"></Checkbox>
      </div>
    </FormElement>
    <DropdownOptionsSelector
      :options="values.options"
      @update="optionUpdated"
      @create="createOption"
      @delete="deleteOption"
    />
  </form>
</template>

<script>
import ApplicationBuilderFormulaInputGroup from '@baserow/modules/builder/components/ApplicationBuilderFormulaInputGroup.vue'
import { DATA_PROVIDERS_ALLOWED_FORM_ELEMENTS } from '@baserow/modules/builder/enums'
import form from '@baserow/modules/core/mixins/form'
import DropdownOptionsSelector from '@baserow/modules/builder/components/elements/components/forms/general/dropdown/DropdownOptionsSelector.vue'
import DropdownDefaultValueSelector from '@baserow/modules/builder/components/elements/components/forms/general/dropdown/DropdownDefaultValueSelector.vue'

export default {
  name: 'DropdownElementForm',
  components: {
    DropdownDefaultValueSelector,
    DropdownOptionsSelector,
    ApplicationBuilderFormulaInputGroup,
  },
  mixins: [form],
  inject: ['page'],
  data() {
    return {
      allowedValues: [
        'label',
        'default_value',
        'required',
        'placeholder',
        'options',
      ],
      values: {
        label: '',
        default_value: null,
        required: false,
        placeholder: '',
        options: [],
      },
    }
  },
  computed: {
    DATA_PROVIDERS_ALLOWED_FORM_ELEMENTS: () =>
      DATA_PROVIDERS_ALLOWED_FORM_ELEMENTS,
    element() {
      return this.$store.getters['element/getElementById'](
        this.page,
        this.defaultValues.id
      )
    },
  },
  watch: {
    'element.options'(options) {
      this.values.options = options.map((o) => o)
    },
  },
  methods: {
    optionUpdated({ id }, changes) {
      const index = this.values.options.findIndex((option) => option.id === id)
      this.$set(this.values.options, index, {
        ...this.values.options[index],
        ...changes,
      })
    },
    createOption() {
      this.values.options.push({ name: '', value: '' })
    },
    deleteOption({ id }) {
      this.values.options = this.values.options.filter(
        (option) => option.id !== id
      )
    },
  },
}
</script>
