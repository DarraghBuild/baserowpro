<template>
  <Modal>
    <h2 class="box__title">{{ $t('addElementModal.title') }}</h2>
    <Search
      class="margin-bottom-2"
      :placeholder="$t('addElementModal.searchPlaceholder')"
      @input="search = $event.target.value"
    />
    <div class="add-element-modal__element-cards">
      <ElementCard
        v-for="elementType in elementTypes"
        :key="elementType.getType()"
        class="add-element-modal__element-card"
        :element-type="elementType"
        @click.native.prevent="addElement(elementType)"
      />
    </div>
  </Modal>
</template>

<script>
import modal from '@baserow/modules/core/mixins/modal'
import ElementCard from '@baserow/modules/builder/components/elements/ElementCard'
import { notifyIf } from '@baserow/modules/core/utils/error'

export default {
  name: 'AddElementModal',
  components: { ElementCard },
  mixins: [modal],
  props: {
    page: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      search: null,
    }
  },
  computed: {
    elementTypes() {
      const allElementTypes = Object.values(this.$registry.getAll('element'))

      if (
        this.search === '' ||
        this.search === null ||
        this.search === undefined
      ) {
        return allElementTypes
      }

      return allElementTypes.filter((elementType) => {
        const nameSanitised = elementType.name.toLowerCase()
        const descriptionSanitised = elementType.description.toLowerCase()
        const searchSanitised = this.search.toLowerCase().trim()

        const matchesName = nameSanitised.includes(searchSanitised)
        const matchesDescription =
          descriptionSanitised.includes(searchSanitised)

        return matchesName || matchesDescription
      })
    },
  },
  methods: {
    async addElement(elementType) {
      try {
        await this.$store.dispatch('element/create', {
          page: this.page,
          elementType,
        })
      } catch (error) {
        notifyIf(error)
      }

      this.$emit('added')
      this.hide()
    },
  },
}
</script>
