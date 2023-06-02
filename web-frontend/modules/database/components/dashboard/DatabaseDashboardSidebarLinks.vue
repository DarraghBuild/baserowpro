<template>
  <li>
    <nuxt-link
      :to="{ name: 'database-api-docs' }"
      class="dashboard__sidebar-link"
    >
      <i class="iconoir-book"></i>
      <span>{{ $t('databaseDashboardSidebarLinks.apiDocumentation') }}</span>
    </nuxt-link>
  </li>
</template>

<script>
export default {
  name: 'DatabaseDashboardSidebarLinks',
}
</script>
