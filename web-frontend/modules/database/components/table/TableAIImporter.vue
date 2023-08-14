<template>
  <div>
    <div class="control">
      <label class="control__label">Description</label>
      <div class="control__description">
        Describe what you would like to see in the table as clear as possible.
      </div>
      <div class="control__elements">
        <textarea
          v-model="values.ai_description"
          class="input input--large textarea--modal"
          :class="{
            'input input--large textarea--modal': true,
            'input--error': $v.values.ai_description.$error,
          }"
          :disabled="isDisabled"
        ></textarea>
        <div v-if="$v.values.ai_description.$error" class="error">
          {{ $t('error.inputRequired') }}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { required } from 'vuelidate/lib/validators'

import form from '@baserow/modules/core/mixins/form'
import importer from '@baserow/modules/database/mixins/importer'

export default {
  name: 'TableAIImporter',
  mixins: [form, importer],
  data() {
    return {
      values: {
        ai_description: '',
      },
    }
  },
  validations: {
    values: {
      ai_description: { required },
    },
  },
  computed: {
    isDisabled() {
      return this.disabled || this.state !== null
    },
  },
  methods: {},
}
</script>
