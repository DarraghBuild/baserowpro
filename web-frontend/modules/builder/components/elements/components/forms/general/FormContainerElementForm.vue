<template>
  <form @submit.prevent @keydown.enter.prevent>
    <FormElement class="control">
      <label class="control__label form-container-element-form__button-label">
        {{ $t('formContainerElementForm.submitButtonLabel') }}
        <i class="iconoir-submit-document"></i>
      </label>
      <Dropdown v-model="values.submitButtonId" :show-search="false">
        <DropdownItem
          v-for="button in buttonsInForm"
          :key="button.id"
          :value="button.id"
          :name="getFormElementName(button)"
          >{{ getFormElementName(button) }}</DropdownItem
        >
      </Dropdown>
    </FormElement>
  </form>
</template>

<script>
import form from '@baserow/modules/core/mixins/form'

export default {
  name: 'FormContainerElementForm',
  mixins: [form],
  inject: ['page'],
  data() {
    return {
      values: {
        submitButtonId: null,
      },
    }
  },
  computed: {
    buttonsInForm() {
      // TODO we still need to filter by button
      return this.$store.getters['element/getChildren'](
        this.page,
        this.defaultValues
      )
    },
  },
  methods: {
    getFormElementName(formElement) {
      const elementType = this.$registry.get('element', formElement.type)
      return elementType.getFormDataName(formElement, { page: this.page })
    },
  },
}
</script>
