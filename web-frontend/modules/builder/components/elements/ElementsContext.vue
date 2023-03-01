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
      :elements="elementsFiltered"
    />
    <AddElementButton @click="$refs.addElementModal.show()" />
    <AddElementModal ref="addElementModal" :page="page" @added="hide()" />
  </Context>
</template>

<script>
import context from '@baserow/modules/core/mixins/context'
import ElementsList from '@baserow/modules/builder/components/elements/ElementsList'
import AddElementButton from '@baserow/modules/builder/components/elements/AddElementButton'
import AddElementModal from '@baserow/modules/builder/components/elements/AddElementModal'
import { mapGetters } from 'vuex'

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
    ...mapGetters({
      page: 'page/getSelected',
      elements: 'element/getElements',
    }),
    elementsFiltered() {
      if (
        this.search === '' ||
        this.search === null ||
        this.search === undefined
      ) {
        return this.elements
      }

      return this.elements.filter((element) => {
        const nameSanitised = element._.elementType.name.toLowerCase()
        const searchSanitised = this.search.toLowerCase().trim()
        return nameSanitised.includes(searchSanitised)
      })
    },
  },
}
</script>
