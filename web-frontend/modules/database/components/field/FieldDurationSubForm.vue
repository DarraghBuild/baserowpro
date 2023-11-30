<template>
  <div>
    <div class="control">
      <label class="control__label control__label--small">{{
        $t('fieldDurationSubForm.durationFormatLabel')
      }}</label>
      <div class="control__elements">
        <Dropdown
          v-model="values.duration_format"
          :class="{ 'dropdown--error': $v.values.duration_format.$error }"
          :fixed-items="true"
          small
          @hide="$v.values.duration_format.$touch()"
        >
          <DropdownItem name="h:mm (1:23)" :value="'h:mm'"></DropdownItem>
          <DropdownItem
            name="h:mm:ss (1:23:40)"
            :value="'h:mm:ss'"
          ></DropdownItem>
          <DropdownItem
            name="h:mm:ss.s (1:23:40.0)"
            :value="'h:mm:ss.s'"
          ></DropdownItem>
          <DropdownItem
            name="h:mm:ss.ss (1:23:40.00)"
            :value="'h:mm:ss.ss'"
          ></DropdownItem>
          <DropdownItem
            name="h:mm:ss.sss (1:23:40.000)"
            :value="'h:mm:ss.sss'"
          ></DropdownItem>
        </Dropdown>
      </div>
    </div>
  </div>
</template>

<script>
import { required } from 'vuelidate/lib/validators'

import form from '@baserow/modules/core/mixins/form'
import fieldSubForm from '@baserow/modules/database/mixins/fieldSubForm'

export default {
  name: 'FieldDurationSubForm',
  mixins: [form, fieldSubForm],
  data() {
    const allowedValues = ['duration_format']
    const values = { duration_format: 'h:mm' }

    return {
      allowedValues,
      values,
    }
  },
  validations: {
    values: {
      duration_format: { required },
    },
  },
}
</script>
