<template>
  <div class="dashboard__group">
    <div class="dashboard__group-head">
      <div
        class="dashboard__group-title"
        :class="{ 'dashboard__group-title--loading': workspace._.loading }"
      >
        <Editable
          ref="rename"
          :value="workspace.name"
          @change="renameWorkspace(workspace, $event)"
        ></Editable>
        <a
          ref="contextLink"
          class="dashboard__group-title-options"
          @click="$refs.context.toggle($refs.contextLink, 'bottom', 'right', 0)"
        >
          <i class="dashboard__group-title-icon iconoir-nav-arrow-down"></i>
        </a>
      </div>
      <WorkspaceContext
        ref="context"
        :workspace="workspace"
        @rename="enableRename()"
      ></WorkspaceContext>
      <div class="dashboard__group-title-extra">
        <component
          :is="component"
          v-for="(component, index) in dashboardWorkspaceExtraComponents"
          :key="index"
          :workspace="workspace"
          :component-arguments="componentArguments"
          @workspace-updated="$emit('workspace-updated', workspace)"
        ></component>
      </div>
    </div>
    <component
      :is="component"
      v-for="(component, index) in dashboardWorkspaceComponents"
      :key="index"
      :workspace="workspace"
      :component-arguments="componentArguments"
    ></component>
    <ul class="dashboard__group-items">
      <li
        v-for="application in getAllOfWorkspace(workspace)"
        :key="application.id"
        class="dashboard__group-item"
      >
        <button
          class="dashboard__group-item-button"
          @click="selectApplication(application)"
        >
          <IconButton :icon="application._.type.iconClass"></IconButton>
          <div class="dashboard__group-item-name">
            {{ application.name }}
          </div>
        </button>
      </li>
      <li class="dashboard__group-item">
        <button
          ref="createApplicationContextLink"
          class="dashboard__group-item-button"
          @click="
            $refs.createApplicationContext.toggle(
              $refs.createApplicationContextLink
            )
          "
        >
          <IconButton icon="plus"></IconButton>

          <div class="dashboard__group-item-name">
            {{ $t('dashboardWorkspace.createApplication') }}
          </div>
        </button>
        <CreateApplicationContext
          ref="createApplicationContext"
          :workspace="workspace"
        ></CreateApplicationContext>
      </li>
    </ul>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

import CreateApplicationContext from '@baserow/modules/core/components/application/CreateApplicationContext'
import WorkspaceContext from '@baserow/modules/core/components/workspace/WorkspaceContext'
import editWorkspace from '@baserow/modules/core/mixins/editWorkspace'

export default {
  components: {
    CreateApplicationContext,
    WorkspaceContext,
  },
  mixins: [editWorkspace],
  props: {
    workspace: {
      type: Object,
      required: true,
    },
    componentArguments: {
      type: Object,
      required: true,
    },
  },
  computed: {
    dashboardWorkspaceExtraComponents() {
      return Object.values(this.$registry.getAll('plugin'))
        .map((plugin) => plugin.getDashboardWorkspaceExtraComponent())
        .filter((component) => component !== null)
    },
    dashboardWorkspaceComponents() {
      return Object.values(this.$registry.getAll('plugin'))
        .map((plugin) => plugin.getDashboardWorkspaceComponent())
        .filter((component) => component !== null)
    },
    ...mapGetters({
      getAllOfWorkspace: 'application/getAllOfWorkspace',
    }),
  },
  methods: {
    selectApplication(application) {
      const type = this.$registry.get('application', application.type)
      type.select(application, this)
    },
  },
}
</script>
