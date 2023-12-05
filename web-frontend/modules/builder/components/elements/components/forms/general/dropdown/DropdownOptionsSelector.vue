<template>
  <FormElement>
    <label class="control__label">
      {{ $t('dropdownOptionSelector.label') }}
    </label>
    <div class="row margin-bottom-1">
      <div class="col col-6">
        {{ $t('dropdownOptionSelector.value') }}
      </div>
      <div class="col col-6">
        {{ $t('dropdownOptionSelector.name') }}
      </div>
    </div>
    <DropdownOption
      v-for="option in options"
      :key="option.id"
      class="margin-bottom-1"
      :option="option"
      @update="$emit('update', option, $event)"
    />
    <Button
      class="margin-top-1"
      size="tiny"
      type="link"
      prepend-icon="baserow-icon-plus"
      :loading="loading"
      @click="$emit('create')"
    >
      {{ $t('dropdownOptionSelector.addOption') }}
    </Button>
  </FormElement>
</template>

<script>
import DropdownOption from '@baserow/modules/builder/components/elements/components/forms/general/dropdown/DropdownOption.vue'
export default {
  name: 'DropdownOptionsSelector',
  components: { DropdownOption },
  props: {
    options: {
      type: Array,
      required: true,
    },
    loading: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
}
</script>
