<template>
  <header class="layout__col-2-1 header header--space-between">
    <ul class="header__filter">
      <li class="header__filter-item">
        <PageHeaderElements />
      </li>
    </ul>
    <DeviceSelector />
  </header>
</template>

<script>
import PageHeaderElements from '@baserow/modules/builder/components/elements/PageHeaderElements'
import DeviceSelector from '@baserow/modules/builder/components/page/components/DeviceSelector'
export default {
  name: 'PageHeader',
  components: { DeviceSelector, PageHeaderElements },
}
</script>
