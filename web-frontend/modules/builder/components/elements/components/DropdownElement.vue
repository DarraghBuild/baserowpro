<template>
  <Dropdown>
    <DropdownItem name="test" value="test"></DropdownItem>
  </Dropdown>
</template>

<script>
import element from '@baserow/modules/builder/store/element'

export default {
  name: 'DropdownElement',
  mixin: [element],
}
</script>
