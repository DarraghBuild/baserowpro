<template>
  <form @submit.prevent="submit">
    <FormInput
      ref="name"
      v-model="values.name"
      :label="$t('workspaceForm.nameLabel')"
      :error="fieldHasErrors('name') ? $t('error.requiredField') : null"
      required
    />
    <slot></slot>
  </form>
</template>

<script>
import { required } from 'vuelidate/lib/validators'

import form from '@baserow/modules/core/mixins/form'

export default {
  name: 'WorkspaceForm',
  mixins: [form],
  props: {
    defaultName: {
      type: String,
      required: false,
      default: '',
    },
  },
  data() {
    return {
      values: {
        name: this.defaultName,
      },
    }
  },
  validations: {
    values: {
      name: { required },
    },
  },
  mounted() {
    this.$refs.name.focus()
  },
}
</script>
