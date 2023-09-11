export class GroupByKey {
  constructor(fieldToValueMap) {
    this.fieldToValueMap = fieldToValueMap
  }

  copyWithExtraValue(fieldToGroupBy, newValue) {
    const newMap = new Map(this.fieldToValueMap)
    newMap[fieldToGroupBy] = newValue
    return new GroupByKey(newMap)
  }

  groupByFieldIdToValueEntriesInOrder() {
    return this.fieldToValueMap.entries()
  }

  toString() {
    const result = []
    for (const [key, value] of this.fieldToValueMap.entries()) {
      result.push(`${key}:${JSON.stringify(value)}`)
    }
    return result.join(',')
  }
}

export class GroupBy {
  constructor(fieldToGroupBy, groupByIsAsc) {
    this.fieldToGroupBy = fieldToGroupBy
    this.groupByIsAsc = groupByIsAsc
  }

  getValueFromRow(row) {
    return row[this.fieldToGroupBy]
  }

  toString() {
    return `${this.fieldToGroupBy}:${this.groupByIsAsc ? 'ASC' : 'DESC'}`
  }
}

export class GroupByTree {
  constructor(groupBys) {
    this.groupBys = groupBys
    this.root = new GroupByNode(this, new GroupByKey(new Map()), 0, null)
  }

  buildFromRows(rows) {
    for (const row of rows) {
      const rowGroupByKey = this.getRowGroupByKey(row)
      this.ensureGroupByNodes(rowGroupByKey)
    }
  }

  getRowGroupByKey(row) {
    const fieldValueMap = new Map()
    for (const groupBy of this.groupBys) {
      fieldValueMap[groupBy.fieldToGroupBy] = groupBy.getValueFromRow(row)
    }
    return new GroupByKey(fieldValueMap)
  }

  ensureGroupByNodes(rowGroupByKey) {
    let node = this.root
    for (const [
      field,
      value,
    ] of rowGroupByKey.groupByFieldIdToValueEntriesInOrder()) {
      node = node.upsertChildNode(field, value)
    }
  }

  toString() {
    const groupBys = this.groupBys
      .map((groupBy) => groupBy.toString())
      .join(',')
    return `GroupByTree(group_bys=${groupBys}, tree=\n${this.root.toString(
      0
    )}\n): `
  }
}

export class GroupByNode {
  constructor(tree, groupKey, count, parent) {
    this.tree = tree
    this.groupKey = groupKey
    this.count = count
    this.parent = parent
    this.collapsed = false
    this.children = new Map()
    this.level = parent == null ? 0 : parent.level + 1
  }

  upsertChildNode(groupByFieldId, childGroupKey) {
    const keyString = childGroupKey.toString()
    const existing = this.children.get(keyString)
    if (existing) {
      return existing
    } else {
      const groupByNode = new GroupByNode(
        this.tree,
        this.groupKey.copyWithExtraValue(groupByFieldId, childGroupKey),
        0,
        this
      )
      this.children.set(keyString, groupByNode)
      return groupByNode
    }
  }

  toString(indentLevel = 0) {
    const indent = '  '.repeat(indentLevel) // Two spaces per indentation level
    let result = `${indent}Node(${this.groupKey.toString()}, count=${
      this.count
    })\n`
    for (const childNode of this.children.values()) {
      result += childNode.toString(indentLevel + 1)
    }
    return result
  }
}
