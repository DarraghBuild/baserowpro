<template>
  <ul class="header__filter">
    <li
      v-for="deviceType in deviceTypes"
      :key="deviceType.getType()"
      class="header__filter-item header__filter-item--no-margin-left"
    >
      <a
        class="header__filter-link"
        :class="{ 'active active--primary': active === deviceType.getType() }"
        @click="active = deviceType.getType()"
      >
        <i :class="`header__filter-icon fas fa-${deviceType.iconClass}`"></i>
      </a>
    </li>
  </ul>
</template>

<script>
export default {
  name: 'DeviceSelector',
  data() {
    return {
      active: null,
    }
  },
  computed: {
    deviceTypes() {
      return Object.values(this.$registry.getAll('device')).sort(
        (a, b) => a.order - b.order
      )
    },
  },
  watch: {
    active: {
      handler(value) {
        this.$store.dispatch('page/setDeviceTypeSelected', value)
      },
      immediate: true,
    },
  },
  created() {
    if (this.deviceTypes.length) {
      this.active = this.deviceTypes[0].getType()
    }
  },
}
</script>
