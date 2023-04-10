<template>
  <CrudTable
    :columns="columns"
    :service="service"
    row-id-key="id"
    @row-context="onRowContext"
  >
    <template #title>
      {{ $t('workspacesAdminTable.allWorkspaces') }}
    </template>
    <template #menus="slotProps">
      <EditWorkspaceContext
        ref="editWorkspaceContext"
        :workspace="editWorkspace"
        @workspace-deleted="slotProps.deleteRow"
      >
      </EditWorkspaceContext>
    </template>
  </CrudTable>
</template>

<script>
import WorkspacesAdminService from '@baserow_premium/services/admin/workspaces'
import CrudTable from '@baserow/modules/core/components/crudTable/CrudTable'
import SimpleField from '@baserow/modules/core/components/crudTable/fields/SimpleField'
import LocalDateField from '@baserow/modules/core/components/crudTable/fields/LocalDateField'
import MoreField from '@baserow/modules/core/components/crudTable/fields/MoreField'
import WorkspaceUsersField from '@baserow_premium/components/admin/workspaces/fields/WorkspaceUsersField'
import WorkspaceNameField from '@baserow_premium/components/admin/workspaces/fields/WorkspaceNameField'
import EditWorkspaceContext from '@baserow_premium/components/admin/workspaces/contexts/EditWorkspaceContext'
import CrudTableColumn from '@baserow/modules/core/crudTable/crudTableColumn'

export default {
  name: 'WorkspacesAdminTable',
  components: {
    CrudTable,
    EditWorkspaceContext,
  },
  data() {
    this.columns = [
      new CrudTableColumn(
        'name',
        () => this.$t('workspacesAdminTable.name'),
        WorkspaceNameField,
        { sortable: true, stickyLeft: true, fixedWidth: 200 }
      ),
      new CrudTableColumn(
        'users',
        () => this.$t('workspacesAdminTable.members'),
        WorkspaceUsersField,
        {}
      ),
      new CrudTableColumn(
        'application_count',
        () => this.$t('workspacesAdminTable.applications'),
        SimpleField,
        { sortable: true }
      ),
      new CrudTableColumn(
        'free_users',
        () => this.$t('workspacesAdminTable.freeUsers'),
        SimpleField,
        {}
      ),
      new CrudTableColumn(
        'seats_taken',
        () => this.$t('workspacesAdminTable.seatsTaken'),
        SimpleField,
        { helpText: this.$t('workspacesAdminTable.usageHelpText') }
      ),
      new CrudTableColumn(
        'row_count',
        () => this.$t('workspacesAdminTable.rowCount'),
        SimpleField,
        {
          sortable: true,
          helpText: this.$t('workspacesAdminTable.usageHelpText'),
        }
      ),
      new CrudTableColumn(
        'storage_usage',
        () => this.$t('workspacesAdminTable.storageUsage'),
        SimpleField,
        {
          sortable: true,
          helpText: this.$t('workspacesAdminTable.usageHelpText'),
        }
      ),
      new CrudTableColumn(
        'created_on',
        () => this.$t('workspacesAdminTable.created'),
        LocalDateField,
        {
          sortable: true,
        }
      ),
      new CrudTableColumn('more', '', MoreField, {
        stickyRight: true,
      }),
    ]
    this.service = WorkspacesAdminService(this.$client)
    return {
      editWorkspace: {},
      hiddenUsers: [],
    }
  },
  methods: {
    onRowContext({ row, event, target }) {
      event.preventDefault()
      if (target === undefined) {
        target = {
          left: event.clientX,
          top: event.clientY,
        }
      }

      const action = row.id === this.editWorkspace.id ? 'toggle' : 'show'
      this.editWorkspace = row
      this.$refs.editWorkspaceContext[action](target, 'bottom', 'left', 4)
    },
  },
}
</script>
