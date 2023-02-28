<template>
  <Context class="elements-context">
    <div class="elements-context__search">
      <Search
        :placeholder="$t('elementsContext.searchPlaceholder')"
        simple
        @input="search = $event.target.value"
      />
    </div>
    <ElementsList
      class="context__menu elements-context__elements-list"
      :elements="elements"
    />
    <AddElementButton @click="$refs.addElementModal.show()" />
    <AddElementModal ref="addElementModal" />
  </Context>
</template>

<script>
import context from '@baserow/modules/core/mixins/context'
import ElementsList from '@baserow/modules/builder/components/elements/ElementsList'
import AddElementButton from '@baserow/modules/builder/components/elements/AddElementButton'
import AddElementModal from '@baserow/modules/builder/components/elements/AddElementModal'

export default {
  name: 'ElementsContext',
  components: { AddElementModal, AddElementButton, ElementsList },
  mixins: [context],
  data() {
    return {
      search: null,
    }
  },
  computed: {
    elements() {
      // TODO Instead of all elements these need to be the elements currently on the
      // page
      const allElements = Object.values(this.$registry.getAll('element'))

      if (
        this.search === '' ||
        this.search === null ||
        this.search === undefined
      ) {
        return allElements
      }

      return allElements.filter((element) => {
        const nameSanitised = element.name.toLowerCase()
        const searchSanitised = this.search.toLowerCase().trim()
        return nameSanitised.includes(searchSanitised)
      })
    },
  },
}
</script>
