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
      v-if="elementsFiltered.length"
      class="context__menu elements-context__elements-list"
      :elements="elementsFiltered"
      @select="selectElement($event)"
    />
    <AddElementButton @click="$refs.addElementModal.show()" />
    <AddElementModal
      ref="addElementModal"
      :loading="loading"
      :page="page"
      @add="addElement"
    />
  </Context>
</template>

<script>
import context from '@baserow/modules/core/mixins/context'
import ElementsList from '@baserow/modules/builder/components/elements/ElementsList'
import AddElementButton from '@baserow/modules/builder/components/elements/AddElementButton'
import AddElementModal from '@baserow/modules/builder/components/elements/AddElementModal'
import { mapActions, mapGetters } from 'vuex'
import { notifyIf } from '@baserow/modules/core/utils/error'

export default {
  name: 'ElementsContext',
  components: { AddElementModal, AddElementButton, ElementsList },
  mixins: [context],
  data() {
    return {
      search: null,
      loading: false,
    }
  },
  computed: {
    ...mapGetters({
      page: 'page/getSelected',
    }),
    elements() {
      return this.$store.getters['element/getElements'](this.page.id)
    },
    elementsFiltered() {
      if (
        this.search === '' ||
        this.search === null ||
        this.search === undefined
      ) {
        return this.elements
      }

      return this.elements.filter((element) => {
        const elementType = this.$registry.get('element', element.type)
        const nameSanitised = elementType.name.toLowerCase()
        const searchSanitised = this.search.toLowerCase().trim()
        return nameSanitised.includes(searchSanitised)
      })
    },
  },
  methods: {
    ...mapActions({
      actionCreateElement: 'element/create',
      actionSelectElement: 'element/select',
    }),
    async addElement(elementType) {
      this.loading = true
      try {
        await this.actionCreateElement({
          pageId: this.page.id,
          elementType: elementType.getType(),
        })
      } catch (error) {
        notifyIf(error)
      }
      this.loading = false
      this.hide()
      this.$refs.addElementModal.hide()
    },
    selectElement(element) {
      this.actionSelectElement({ element })
      this.hide()
    },
  },
}
</script>
