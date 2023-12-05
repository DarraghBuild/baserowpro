<template>
  <Dropdown :disabled="mode === 'editing'">
    <DropdownItem name="test" value="test"></DropdownItem>
  </Dropdown>
</template>

<script>
import formElement from '@baserow/modules/builder/mixins/formElement'

export default {
  name: 'DropdownElement',
  mixins: [formElement],
}
</script>
