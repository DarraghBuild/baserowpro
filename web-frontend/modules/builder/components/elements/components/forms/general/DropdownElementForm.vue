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
      :options="options"
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
      :options="options"
      :loading="creatingOption"
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
import { mapActions } from 'vuex'
import _ from 'lodash'

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
      allowedValues: ['label', 'default_value', 'required', 'placeholder'],
      values: {
        label: '',
        default_value: null,
        required: false,
        placeholder: '',
      },
      options: [],
      creatingOption: false,
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
  mounted() {
    this.options = _.clone(this.element.options)
  },
  methods: {
    ...mapActions({
      actionDebouncedUpdateSelected: 'element/debouncedUpdateSelected',
    }),
    optionUpdated({ id }, changes) {
      const optionIndex = this.options.findIndex((option) => option.id === id)
      this.$set(this.options, optionIndex, {
        ...this.options[optionIndex],
        ...changes,
      })

      this.actionDebouncedUpdateSelected({
        page: this.page,
        values: { options: _.clone(this.options) },
      })
    },
    async createOption() {
      this.creatingOption = true
      const newOption = { name: '', value: '' }

      await this.actionDebouncedUpdateSelected({
        page: this.page,
        values: { options: [...this.options, newOption] },
      })

      this.options = _.clone(this.element.options)
      this.creatingOption = false
    },
    deleteOption({ id }) {
      this.options = this.options.filter((option) => option.id !== id)
      this.actionDebouncedUpdateSelected({
        page: this.page,
        values: { options: _.clone(this.options) },
      })
    },
  },
}
</script>
