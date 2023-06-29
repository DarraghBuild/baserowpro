import { TestApp } from '@baserow/test/helpers/testApp'
import { firstBy } from 'thenby'

const string_a = { id: 1, value: 'a' }
const string_b = { id: 2, value: 'b' }
const string_aa = { id: 3, value: 'aa' }
const string_aaa = { id: 5, value: 'aaa' }
const string_null = { id: 6, value: '' }

const number_1 = { id: 1, value: '1' }
const number_2 = { id: 2, value: '2' }
const number_11 = { id: 3, value: '11' }
const number_111 = { id: 4, value: '111' }
const number_null = { id: 5, value: null }

const number_f_0_0_5 = { id: 1, value: '0.05' }
const number_f_0_4 = { id: 2, value: '0.40' }
const number_f_1_0 = { id: 3, value: '1.00' }
const number_f_1_1 = { id: 4, value: '1.10' }
const number_f_null = { id: 5, value: null }

const boolean_true = { id: 1, value: true }
const boolean_false = { id: 2, value: false }

const ArrayOfArraysTable = [
  {
    id: 1,
    order: '1.00000000000000000000',
    field_strings: [string_b, string_a],
    field_numbers: [number_2, number_1],
    field_booleans: [boolean_false, boolean_true],
    field_numbers_fractions: [number_f_0_4, number_f_0_0_5],
  },
  {
    id: 2,
    order: '2.00000000000000000000',
    field_strings: [string_a],
    field_numbers: [number_1],
    field_booleans: [boolean_true],
    field_numbers_fractions: [number_f_0_0_5],
  },
  {
    id: 3,
    order: '3.00000000000000000000',
    field_strings: [string_a, string_b],
    field_numbers: [number_1, number_2],
    field_booleans: [boolean_true, boolean_false],
    field_numbers_fractions: [number_f_0_0_5, number_f_0_4],
  },
  {
    id: 4,
    order: '4.00000000000000000000',
    field_strings: [],
    field_numbers: [],
    field_booleans: [],
    field_numbers_fractions: [],
  },
  {
    id: 5,
    order: '5.00000000000000000000',
    field_strings: [string_b, string_aaa],
    field_numbers: [number_2, number_111],
    field_booleans: [boolean_false, boolean_true],
    field_numbers_fractions: [number_f_0_4, number_f_1_1],
  },
  {
    id: 6,
    order: '6.00000000000000000000',
    field_strings: [string_a],
    field_numbers: [number_1],
    field_booleans: [boolean_true],
    field_numbers_fractions: [number_f_0_4],
  },
  {
    id: 7,
    order: '7.00000000000000000000',
    field_strings: [string_aa],
    field_numbers: [number_11],
    field_booleans: [boolean_true],
    field_numbers_fractions: [number_f_1_0],
  },
  {
    id: 8,
    order: '8.00000000000000000000',
    field_strings: [string_null, string_a],
    field_numbers: [number_null, number_1],
    field_booleans: [boolean_false, boolean_true],
    field_numbers_fractions: [number_f_null, number_f_0_0_5],
  },
]

describe('FormulaFieldType.getSort()', () => {
  let testApp = null

  beforeAll(() => {
    testApp = new TestApp()
  })

  afterEach(() => {
    testApp.afterEach()
  })

  test('array(text)', () => {
    const formulaType = testApp._app.$registry.get('field', 'formula')
    const formulaField = {
      formula_type: 'array',
      array_formula_type: 'text',
    }

    expect(formulaType.getCanSortInView(formulaField)).toBe(true)

    const ASC = formulaType.getSort('field_strings', 'ASC', formulaField)
    const sortASC = firstBy().thenBy(ASC)
    const DESC = formulaType.getSort('field_strings', 'DESC', formulaField)
    const sortDESC = firstBy().thenBy(DESC)

    ArrayOfArraysTable.sort(sortASC)

    const sorted = ArrayOfArraysTable.map((obj) =>
      obj.field_strings.map((inner) => inner.value)
    )
    const expected = [
      [],
      ['', 'a'],
      ['a'],
      ['a'],
      ['a', 'b'],
      ['aa'],
      ['b', 'a'],
      ['b', 'aaa'],
    ]

    expect(sorted).toEqual(expected)

    ArrayOfArraysTable.sort(sortDESC)

    const sortedReversed = ArrayOfArraysTable.map((obj) =>
      obj.field_strings.map((inner) => inner.value)
    )

    expect(sortedReversed).toEqual(expected.reverse())
  })

  test('array(number)', () => {
    const formulaType = testApp._app.$registry.get('field', 'formula')
    const formulaField = {
      formula_type: 'array',
      array_formula_type: 'number',
    }

    expect(formulaType.getCanSortInView(formulaField)).toBe(true)

    const ASC = formulaType.getSort('field_numbers', 'ASC', formulaField)
    const sortASC = firstBy().thenBy(ASC)
    const DESC = formulaType.getSort('field_numbers', 'DESC', formulaField)
    const sortDESC = firstBy().thenBy(DESC)

    ArrayOfArraysTable.sort(sortASC)

    const sorted = ArrayOfArraysTable.map((obj) =>
      obj.field_numbers.map((inner) => inner.value)
    )
    const expected = [
      [],
      [null, '1'],
      ['1'],
      ['1'],
      ['1', '2'],
      ['2', '1'],
      ['2', '111'],
      ['11'],
    ]

    expect(sorted).toEqual(expected)

    ArrayOfArraysTable.sort(sortDESC)

    const sortedReversed = ArrayOfArraysTable.map((obj) =>
      obj.field_numbers.map((inner) => inner.value)
    )

    expect(sortedReversed).toEqual(expected.reverse())
  })

  test.only('array(number) fractions', () => {
    const formulaType = testApp._app.$registry.get('field', 'formula')
    const formulaField = {
      formula_type: 'array',
      array_formula_type: 'number',
    }

    expect(formulaType.getCanSortInView(formulaField)).toBe(true)

    const ASC = formulaType.getSort(
      'field_numbers_fractions',
      'ASC',
      formulaField
    )
    const sortASC = firstBy().thenBy(ASC)
    const DESC = formulaType.getSort(
      'field_numbers_fractions',
      'DESC',
      formulaField
    )
    const sortDESC = firstBy().thenBy(DESC)

    ArrayOfArraysTable.sort(sortASC)

    const sorted = ArrayOfArraysTable.map((obj) =>
      obj.field_numbers_fractions.map((inner) => inner.value)
    )

    const expected = [
      [],
      [null, '0.05'],
      ['0.05'],
      ['0.05', '0.40'],
      ['0.40'],
      ['0.40', '0.05'],
      ['0.40', '1.10'],
      ['1.00'],
    ]

    expect(sorted).toEqual(expected)

    ArrayOfArraysTable.sort(sortDESC)

    const sortedReversed = ArrayOfArraysTable.map((obj) =>
      obj.field_numbers_fractions.map((inner) => inner.value)
    )

    expect(sortedReversed).toEqual(expected.reverse())
  })

  test('array(boolean)', () => {
    const formulaType = testApp._app.$registry.get('field', 'formula')
    const formulaField = {
      formula_type: 'array',
      array_formula_type: 'boolean',
    }

    expect(formulaType.getCanSortInView(formulaField)).toBe(true)

    const ASC = formulaType.getSort('field_booleans', 'ASC', formulaField)
    const sortASC = firstBy().thenBy(ASC)
    const DESC = formulaType.getSort('field_booleans', 'DESC', formulaField)
    const sortDESC = firstBy().thenBy(DESC)

    ArrayOfArraysTable.sort(sortASC)

    const sorted = ArrayOfArraysTable.map((obj) =>
      obj.field_booleans.map((inner) => inner.value)
    )

    const expected = [
      [],
      [false, true],
      [false, true],
      [false, true],
      [true],
      [true],
      [true],
      [true, false],
    ]

    expect(sorted).toEqual(expected)

    ArrayOfArraysTable.sort(sortDESC)

    const sortedReversed = ArrayOfArraysTable.map((obj) =>
      obj.field_booleans.map((inner) => inner.value)
    )

    expect(sortedReversed).toEqual(expected.reverse())
  })
})
