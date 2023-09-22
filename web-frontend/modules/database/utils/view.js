import { firstBy } from 'thenby'
import BigNumber from 'bignumber.js'
import { maxPossibleOrderValue } from '@baserow/modules/database/viewTypes'
import { escapeRegExp } from '@baserow/modules/core/utils/string'
import { SearchModes } from '@baserow/modules/database/utils/search'
import { convertStringToMatchBackendTsvectorData } from '@baserow/modules/database/search/regexes'

/**
 * Generates a sort function based on the provided sortings.
 */
export function getRowSortFunction($registry, sortings, fields, groupBys = []) {
  let sortFunction = firstBy()
  const combined = [...groupBys, ...sortings]
  combined.forEach((sort) => {
    // Find the field that is related to the sort.
    const field = fields.find((f) => f.id === sort.field)

    if (field !== undefined) {
      const fieldName = `field_${field.id}`
      const fieldType = $registry.get('field', field.type)
      const fieldSortFunction = fieldType.getSort(fieldName, sort.order, field)
      sortFunction = sortFunction.thenBy(fieldSortFunction)
    }
  })

  sortFunction = sortFunction.thenBy((a, b) =>
    new BigNumber(a.order).minus(new BigNumber(b.order))
  )
  sortFunction = sortFunction.thenBy((a, b) => a.id - b.id)
  return sortFunction
}

/**
 * Generates a sort function for fields based on order and id.
 */
export function sortFieldsByOrderAndIdFunction(
  fieldOptions,
  primaryAlwaysFirst = false
) {
  return (a, b) => {
    if (primaryAlwaysFirst) {
      // If primary must always be first, then first by primary.
      if (a.primary > b.primary) {
        return -1
      } else if (a.primary < b.primary) {
        return 1
      }
    }

    const orderA = fieldOptions[a.id]
      ? fieldOptions[a.id].order
      : maxPossibleOrderValue
    const orderB = fieldOptions[b.id]
      ? fieldOptions[b.id].order
      : maxPossibleOrderValue

    // First by order.
    if (orderA > orderB) {
      return 1
    } else if (orderA < orderB) {
      return -1
    }

    // Then by id.
    return a.id - b.id
  }
}

/**
 * Returns only fields that are visible (not hidden).
 */
export function filterVisibleFieldsFunction(fieldOptions) {
  return (field) => {
    const exists = Object.prototype.hasOwnProperty.call(fieldOptions, field.id)
    return !exists || !fieldOptions[field.id].hidden
  }
}

/**
 * Returns only fields that are visible (not hidden).
 */
export function filterHiddenFieldsFunction(fieldOptions) {
  return (field) => {
    const exists = Object.prototype.hasOwnProperty.call(fieldOptions, field.id)
    return exists && fieldOptions[field.id].hidden
  }
}

/**
 * A helper function that checks if the provided row values match the provided view
 * filters. Returning false indicates that the row should not be visible for that
 * view.
 */
export const matchSearchFilters = (
  $registry,
  filterType,
  filters,
  fields,
  values
) => {
  // If there aren't any filters then it is not possible to check if the row
  // matches any of the filters, so we can mark it as valid.
  if (filters.length === 0) {
    return true
  }

  for (const i in filters) {
    const filter = filters[i]
    const filterValue = filter.value
    const rowValue = values[`field_${filter.field}`]
    const field = fields.find((f) => f.id === filter.field)
    const fieldType = $registry.get('field', field.type)
    const matches = $registry
      .get('viewFilter', filter.type)
      .matches(rowValue, filterValue, field, fieldType)
    if (filterType === 'AND' && !matches) {
      // With an `AND` filter type, the row must match all the filters, so if
      // one of the filters doesn't match we can mark it as isvalid.
      return false
    } else if (filterType === 'OR' && matches) {
      // With an 'OR' filter type, the row only has to match one of the filters,
      // that is the case here so we can mark it as valid.
      return true
    }
  }

  if (filterType === 'AND') {
    // When this point has been reached with an `AND` filter type it means that
    // the row matches all the filters and therefore we can mark it as valid.
    return true
  } else if (filterType === 'OR') {
    // When this point has been reached with an `OR` filter type it means that
    // the row matches none of the filters and therefore we can mark it as invalid.
    return false
  }
}

function _fullTextSearch(registry, field, value, activeSearchTerm) {
  const searchableString = registry
    .get('field', field.type)
    .toSearchableString(field, value)
  const fixedValue = convertStringToMatchBackendTsvectorData(searchableString)
  const fixedTerm = convertStringToMatchBackendTsvectorData(activeSearchTerm)
  if (fixedTerm.length === 0) {
    return false
  } else {
    const regexMatchingWordsThatStartWithTerm =
      '(^|\\s+)' + escapeRegExp(fixedTerm)
    return !!fixedValue.match(
      new RegExp(regexMatchingWordsThatStartWithTerm, 'gu')
    )
  }
}

function _compatSearchMode(registry, field, value, activeSearchTerm) {
  return registry
    .get('field', field.type)
    .containsFilter(value, activeSearchTerm, field)
}

export function valueMatchesActiveSearchTerm(
  searchMode,
  registry,
  field,
  value,
  activeSearchTerm
) {
  if (searchMode === SearchModes.MODE_FT_WITH_COUNT) {
    return _fullTextSearch(registry, field, value, activeSearchTerm)
  } else {
    return _compatSearchMode(registry, field, value, activeSearchTerm)
  }
}

function _findFieldsInRowMatchingSearch(
  row,
  activeSearchTerm,
  fields,
  registry,
  overrides,
  searchMode
) {
  const fieldSearchMatches = new Set()
  // If the row is loading then a temporary UUID is put in its id. We don't want to
  // accidentally match against that UUID as it will be shortly replaced with its
  // real id.
  if (
    !row._.loading &&
    row.id?.toString() === (activeSearchTerm || '').trim()
  ) {
    fieldSearchMatches.add('row_id')
  }
  for (const field of fields) {
    const fieldName = `field_${field.id}`
    const rowValue =
      fieldName in overrides ? overrides[fieldName] : row[fieldName]
    if (rowValue !== undefined && rowValue !== null) {
      const doesMatch = valueMatchesActiveSearchTerm(
        searchMode,
        registry,
        field,
        rowValue,
        activeSearchTerm
      )
      if (doesMatch) {
        fieldSearchMatches.add(field.id.toString())
      }
    }
  }

  return fieldSearchMatches
}

/**
 * Helper function which calculates if a given row and which of it's fields matches a
 * given search term. The rows values can be overridden by providing an overrides
 * object containing a mapping of the field name to override to a value that will be
 * used to check for matches instead of the rows real one. The rows values will not be
 * changed.
 */
export function calculateSingleRowSearchMatches(
  row,
  activeSearchTerm,
  hideRowsNotMatchingSearch,
  fields,
  registry,
  searchMode,
  overrides = {}
) {
  const searchIsBlank = activeSearchTerm === ''
  const fieldSearchMatches = searchIsBlank
    ? new Set()
    : _findFieldsInRowMatchingSearch(
        row,
        activeSearchTerm,
        fields,
        registry,
        overrides,
        searchMode
      )

  const matchSearch =
    !hideRowsNotMatchingSearch || searchIsBlank || fieldSearchMatches.size > 0
  return { row, matchSearch, fieldSearchMatches }
}

/**
 * Returns true is the empty value of the provided field matches the active search term.
 */
export function newFieldMatchesActiveSearchTerm(
  registry,
  newField,
  activeSearchTerm
) {
  if (newField && activeSearchTerm !== '') {
    const fieldType = registry.get('field', newField.type)
    const emptyValue = fieldType.getEmptyValue(newField)

    return valueMatchesActiveSearchTerm(
      registry,
      newField,
      emptyValue,
      activeSearchTerm
    )
  }
  return false
}

export function getOrderBy(rootGetters, viewId) {
  if (rootGetters['page/view/public/getIsPublic']) {
    const view = rootGetters['view/get'](viewId)
    return view.sortings
      .map((sort) => {
        return `${sort.order === 'DESC' ? '-' : ''}field_${sort.field}`
      })
      .join(',')
  } else {
    return ''
  }
}

export function getFilters(rootGetters, viewId) {
  const filters = {}

  if (rootGetters['page/view/public/getIsPublic']) {
    const view = rootGetters['view/get'](viewId)

    if (!view.filters_disabled) {
      view.filters.forEach((filter) => {
        const name = `filter__field_${filter.field}__${filter.type}`
        if (!Object.prototype.hasOwnProperty.call(filters, name)) {
          filters[name] = []
        }
        filters[name].push(filter.value)
      })
    }

    filters.filter_type = [view.filter_type]
  }

  return filters
}

/**
 * Calculates the size of a UTF-8 encoded string in bytes - computes the size
 * of a string in UTF-8 encoding and utilizes the TextEncoder API if available.
 *
 * Using TextEncoder is preferred in Modern Browsers and Node.js Supported
 * environments because it provides a more efficient and accurate way to encode
 * strings into UTF-8 bytes and directly calculate the byte size of the encoded
 * string.
 *
 * In some older web browsers or environments where TextEncoder may not be available
 * (such as SSR where certain browser APIs are absent), it falls back to a less
 * accurate method and simply returns the length of the string.
 */
export function utf8ByteSize(str) {
  // Use TextEncoder if available (modern browsers and Node.js)
  if (typeof TextEncoder !== 'undefined') {
    const encoder = new TextEncoder()
    const data = encoder.encode(str)
    return data.length
  } else {
    // Fallback for older browsers (may not be as accurate)
    return str.length
  }
}

/**
 * Limit the size of a cookie's value by removing elements from an array
 * until it fits within the maximum allowed cookie size.
 */
export function fitInCookie(name, list) {
  const result = []
  for (let i = list.length - 1; i >= 0; i--) {
    result.unshift(list[i])
    const serialized = encodeURIComponent(JSON.stringify(result))
    if (utf8ByteSize(serialized) > 4096) {
      result.shift() // Remove the last added item as it caused the size to exceed the limit
      break
    }
  }
  return result
}
