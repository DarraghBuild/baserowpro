export class GroupKey {
  constructor(fieldToValueObject) {
    this.fieldToValueObject = fieldToValueObject
  }
}

export class UnknownGroupsKey {}

class KnownGroupRegion {
  constructor({ key, count, regionIndex }) {
    this.key = key
    this.count = count
    this.regionIndex = regionIndex
  }
}

class UnknownRegion {
  constructor({ count, groupIndex }) {
    this.count = count
  }
}

export class RowRegionTracker {
  constructor() {
    this._explicitlyExpandedGroups = {}
    this._explicitlyCollapsedGroups = {}
    this._knownGroups = []
  }

  fetchRows({ offset, limit, bufferStart, bufferEnd }) {
    return {
      rowsQuery: { offset, limit, collapseTheseGroups: [] },
      groupedRowsQuery: null,
    }
  }
}
