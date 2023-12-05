<template>
  <form @submit.prevent @keydown.enter.prevent>
    <ApplicationBuilderFormulaInputGroup
      v-model="values.label"
      :label="$t('generalForm.labelTitle')"
      :placeholder="$t('generalForm.labelPlaceholder')"
      :data-providers-allowed="DATA_PROVIDERS_ALLOWED_FORM_ELEMENTS"
    ></ApplicationBuilderFormulaInputGroup>
    <ApplicationBuilderFormulaInputGroup
      v-model="values.default_value"
      :label="$t('generalForm.valueTitle')"
      :placeholder="$t('generalForm.valuePlaceholder')"
      :data-providers-allowed="DATA_PROVIDERS_ALLOWED_FORM_ELEMENTS"
    ></ApplicationBuilderFormulaInputGroup>
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
    />
  </form>
</template>

<script>
import ApplicationBuilderFormulaInputGroup from '@baserow/modules/builder/components/ApplicationBuilderFormulaInputGroup.vue'
import { DATA_PROVIDERS_ALLOWED_FORM_ELEMENTS } from '@baserow/modules/builder/enums'
import form from '@baserow/modules/core/mixins/form'
import DropdownOptionsSelector from '@baserow/modules/builder/components/elements/components/forms/general/dropdown/DropdownOptionsSelector.vue'

export default {
  name: 'DropdownElementForm',
  components: { DropdownOptionsSelector, ApplicationBuilderFormulaInputGroup },
  mixins: [form],
  data() {
    return {
      values: {
        label: '',
        default_value: '',
        required: false,
        placeholder: '',
        options: [],
      },
    }
  },
  computed: {
    DATA_PROVIDERS_ALLOWED_FORM_ELEMENTS: () =>
      DATA_PROVIDERS_ALLOWED_FORM_ELEMENTS,
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
      this.values.options.push({ name: null, value: null })
    },
  },
}
</script>
