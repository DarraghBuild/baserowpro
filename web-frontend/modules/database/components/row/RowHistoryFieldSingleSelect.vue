<template>
  <div class="row-history-entry__field-content">
    <div>
      <div
        v-if="entry.before[fieldIdentifier]"
        class="row-history-field-select-option__diff row-history-field-select-option__diff--removed"
      >
        <div
          class="row-history-field-select-option__diff-inner"
          :class="'background-color--' + entry.before[fieldIdentifier].color"
        >
          {{ entry.before[fieldIdentifier].value }}
        </div>
      </div>
    </div>
    <div>
      <div
        v-if="entry.after[fieldIdentifier]"
        class="row-history-field-select-option__diff row-history-field-select-option__diff--added"
      >
        <div
          class="row-history-field-select-option__diff-inner"
          :class="'background-color--' + entry.after[fieldIdentifier].color"
        >
          {{ entry.after[fieldIdentifier].value }}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'RowHistoryFieldSingleSelect',
  props: {
    entry: {
      type: Object,
      required: true,
    },
    fieldIdentifier: {
      type: String,
      required: true,
    },
  },
}
</script>
