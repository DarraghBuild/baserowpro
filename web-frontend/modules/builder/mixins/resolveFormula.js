import RuntimeFormulaContext from '@baserow/modules/core/runtimeFormulaContext'
import { resolveFormula } from '@baserow/modules/core/formula'

export default {
  inject: ['builder', 'page', 'mode'],
  computed: {
    applicationContext() {
      return {
        builder: this.builder,
        page: this.page,
        mode: this.mode,
      }
    },
    runtimeFormulaContext() {
      /**
       * This proxy allow the RuntimeFormulaContextClass to act like a regular object.
       */
      return new Proxy(
        new RuntimeFormulaContext(
          this.$registry.getAll('builderDataProvider'),
          this.applicationContext
        ),
        {
          get(target, prop) {
            return target.get(prop)
          },
        }
      )
    },
    formulaFunctions() {
      return {
        get: (name) => {
          return this.$registry.get('runtimeFormulaFunction', name)
        },
      }
    },
  },
  methods: {
    resolveFormula(formula) {
      try {
        return resolveFormula(
          formula,
          this.formulaFunctions,
          this.runtimeFormulaContext
        )
      } catch (e) {
        return ''
      }
    },
  },
}
