<template>
  <div class="row">
    <div class="col col-5">
      <ApplicationBuilderFormulaInputGroup
        :value="option.value"
        :data-providers-allowed="DATA_PROVIDERS_ALLOWED_FORM_ELEMENTS"
        @input="$emit('update', { value: $event })"
      />
    </div>
    <div class="col col-5">
      <ApplicationBuilderFormulaInputGroup
        :value="option.name"
        :data-providers-allowed="DATA_PROVIDERS_ALLOWED_FORM_ELEMENTS"
        @input="$emit('update', { name: $event })"
      />
    </div>
    <div class="dropdown-option__delete col col-1">
      <Button
        class="control"
        tag="a"
        icon="iconoir-trash"
        type="ghost"
        @click="$emit('delete')"
      ></Button>
    </div>
  </div>
</template>

<script>
import ApplicationBuilderFormulaInputGroup from '@baserow/modules/builder/components/ApplicationBuilderFormulaInputGroup.vue'
import { DATA_PROVIDERS_ALLOWED_FORM_ELEMENTS } from '@baserow/modules/builder/enums'

export default {
  name: 'DropdownOption',
  components: { ApplicationBuilderFormulaInputGroup },
  props: {
    option: {
      type: Object,
      required: true,
    },
  },
  computed: {
    DATA_PROVIDERS_ALLOWED_FORM_ELEMENTS: () =>
      DATA_PROVIDERS_ALLOWED_FORM_ELEMENTS,
  },
}
</script>
