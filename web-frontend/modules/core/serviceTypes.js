import { Registerable } from '@baserow/modules/core/registry'

export class ServiceType extends Registerable {
  get name() {
    throw new Error('Must be set on the type.')
  }

  /**
   * The integration type necessary to access this service.
   */
  get integrationType() {
    throw new Error('Must be set on the type.')
  }

  /**
   * The form component to edit this service.
   */
  get formComponent() {
    return null
  }

  isValid(service) {
    return true
  }

  /**
   * Whether the service returns a collection of records.
   */
  get returnsList() {
    return false
  }

  /**
   * Should return a JSON schema of the data returned by this data source.
   */
  getDataSchema(applicationContext, dataSource) {
    throw new Error('Must be set on the type.')
  }

  getOrder() {
    return 0
  }
}
