<template>
  <div class="context" :class="{ 'visibility-hidden': !open || !updatedOnce }">
    <header v-show="hasHeaderSlot" ref="header" class="context__header">
      <slot name="header"></slot>
    </header>
    <main
      ref="mainContainer"
      class="context__main"
      :style="{ 'overflow-y': overflowY }"
    >
      <slot v-if="openedOnce"></slot>
    </main>
    <footer v-if="hasFooterSlot" ref="footer" class="context__footer">
      <slot name="footer"></slot>
    </footer>
  </div>
</template>

<script>
import {
  isElement,
  isDomElement,
  onClickOutside,
} from '@baserow/modules/core/utils/dom'

import MoveToBody from '@baserow/modules/core/mixins/moveToBody'

export default {
  name: 'Context',
  mixins: [MoveToBody],
  props: {
    hideOnClickOutside: {
      type: Boolean,
      default: true,
      required: false,
    },
  },
  data() {
    return {
      open: false,
      opener: null,
      updatedOnce: false,
      // If opened once, should stay in DOM to keep nested content
      openedOnce: false,
      overflowY: 'auto',
      isScrollable: false,
      mutationObserver: null,
      // space between the edge of the viewport and the context menu
      viewportVerticalOffset: 25,
    }
  },
  computed: {
    hasFooterSlot() {
      return !!this.$slots.footer
    },
    hasHeaderSlot() {
      return !!this.$slots.header
    },
  },
  methods: {
    /** This method listen to the added/removed element dom element
      within the context main container, so we can check if
      the content is scrollable or not */
    listenContentDomChanges() {
      const targetNode = this.$refs.mainContainer
      const observerOptions = {
        childList: true,
        subtree: true,
      }
      this.mutationObserver = new MutationObserver((mutationList, observer) => {
        mutationList.forEach((mutation) => {
          switch (mutation.type) {
            case 'childList':
              this.isScrollable = this.isContentScrollable()
              break
          }
        })
      })
      this.mutationObserver.observe(targetNode, observerOptions)
    },
    /**
     * Toggles the open state of the context menu.
     *
     * @param target      The original element that changed the state of the
     *                    context, this will be used to calculate the correct position.
     * @param vertical    Bottom positions the context under the target.
     *                    Top positions the context above the target.
     *                    Over-bottom positions the context over and under the target.
     *                    Over-top positions the context over and above the target.
     * @param horizontal  `left` aligns the context with the left side of the target.
     *                    `right` aligns the context with the right side of the target.
     * @param verticalOffset
     *                    The offset indicates how many pixels the context is moved
     *                    top from the original calculated position.
     * @param horizontalOffset
     *                    The offset indicates how many pixels the context is moved
     *                    left from the original calculated position.
     * @param value       True if context must be shown, false if not and undefine
     *                    will invert the current state.
     */
    toggle(
      target,
      vertical = 'bottom',
      horizontal = 'left',
      verticalOffset = 10,
      horizontalOffset = 0,
      value
    ) {
      if (value === undefined) {
        value = !this.open
      }

      if (value) {
        this.show(
          target,
          vertical,
          horizontal,
          verticalOffset,
          horizontalOffset
        )
      } else {
        this.hide()
      }
    },
    /**
     * Calculate the position, show the context menu and register a click event on the
     * body to check if the user has clicked outside the context.
     */
    async show(
      target,
      vertical,
      horizontal,
      verticalOffset = 10,
      horizontalOffset = 0
    ) {
      const isElementOrigin = isDomElement(target)

      // If we store the element who opened the context menu we can exclude the element
      // when clicked outside of this element.
      this.opener = isElementOrigin ? target : null

      this.open = true
      this.openedOnce = true

      // Delay the position update to the next tick to let the Context content
      // be available in DOM for accurate positioning.
      await this.$nextTick()
      this.updatePosition(
        target,
        vertical,
        horizontal,
        verticalOffset,
        horizontalOffset
      )

      this.$el.cancelOnClickOutside = onClickOutside(this.$el, (target) => {
        if (
          this.open &&
          // If the prop allows it to be closed by clicking outside.
          this.hideOnClickOutside &&
          // If the click was not on the opener because he can trigger the toggle
          // method.
          !isElement(this.opener, target) &&
          // If the click was not inside one of the context children of this context
          // menu.
          !this.moveToBody.children.some((child) => {
            return isElement(child.$el, target)
          })
        ) {
          this.hide()
        }
      })

      this.$el.updatePositionEvent = (event) => {
        // if scroll is triggered by the context menu itself, we don't need to update
        if (event.target.classList?.contains('context__main')) return

        this.updatePosition(
          target,
          vertical,
          horizontal,
          verticalOffset,
          horizontalOffset
        )
      }

      window.addEventListener('scroll', this.$el.updatePositionEvent, true)
      window.addEventListener('resize', this.$el.updatePositionEvent)

      this.$emit('shown')

      await this.$nextTick()
      this.isScrollable = this.isContentScrollable()
      this.listenContentDomChanges()
    },
    /**
     * Toggles context menu next to mouse when click event has happened
     */
    toggleNextToMouse(
      clickEvent,
      vertical = 'bottom',
      horizontal = 'right',
      verticalOffset = 10,
      horizontalOffset = 0,
      value = true
    ) {
      this.toggle(
        {
          top: clickEvent.pageY,
          left: clickEvent.pageX,
        },
        vertical,
        horizontal,
        verticalOffset,
        horizontalOffset,
        value
      )
    },
    /**
     * Shows context menu next to mouse when click event has happened
     */
    showNextToMouse(
      clickEvent,
      vertical = 'bottom',
      horizontal = 'right',
      verticalOffset = 10,
      horizontalOffset = 0
    ) {
      this.show(
        {
          top: clickEvent.pageY,
          left: clickEvent.pageX,
        },
        vertical,
        horizontal,
        verticalOffset,
        horizontalOffset
      )
    },
    /**
     * Forces the child elements to render by setting `openedOnce` to `true`. This
     * could be useful when children of the context must be accessed before the context
     * has been opened.
     */
    forceRender() {
      this.openedOnce = true
    },
    /**
     * Hide the context menu and make sure the body event is removed.
     */
    hide(emit = true) {
      this.opener = null
      this.open = false

      if (emit) {
        this.$emit('hidden')
      }

      // If the context menu was never opened, it doesn't have the
      // `cancelOnClickOutside`, so we can't call it.
      if (
        Object.prototype.hasOwnProperty.call(this.$el, 'cancelOnClickOutside')
      ) {
        this.$el.cancelOnClickOutside()
      }
      this.mutationObserver?.disconnect()
      window.removeEventListener('scroll', this.$el.updatePositionEvent, true)
      window.removeEventListener('resize', this.$el.updatePositionEvent)
    },
    /**
     * Calculates the absolute position of the context based on the original clicked
     * element. If the target element is not visible, it might mean that we can't
     * figure out the correct position, so in that case we force the element to be
     * visible.
     */
    calculatePositionElement(
      target,
      vertical,
      horizontal,
      verticalOffset,
      horizontalOffset
    ) {
      const visible =
        window.getComputedStyle(target).getPropertyValue('display') !== 'none'

      this.$el.style.width = 'auto'

      // If the target is not visible then we can't calculate the position, so we
      // temporarily need to shw the element forcefully.
      if (!visible) target.classList.add('forced-block')
      const targetRect = target.getBoundingClientRect()

      const positions = { top: null, right: null, bottom: null, left: null }

      // Take into account that the document might be scrollable.
      verticalOffset += document.documentElement.scrollTop
      horizontalOffset += document.documentElement.scrollLeft

      const { vertical: verticalAdjusted, horizontal: horizontalAdjusted } =
        this.checkForEdges(
          targetRect,
          vertical,
          horizontal,
          verticalOffset,
          horizontalOffset
        )

      // Calculate the correct positions for horizontal and vertical values.
      if (horizontalAdjusted === 'left') {
        positions.transform = 'none'
        positions.left = `${targetRect.left + horizontalOffset}px`
      }

      if (horizontalAdjusted === 'right') {
        positions.transform = 'none'
        positions.right = `${
          window.innerWidth - targetRect.right - horizontalOffset
        }px`
      }

      // in case there is no enough space on the right and left
      // we horizontally center the context menu in the viewport
      if (horizontalAdjusted === 'window') {
        positions.left = '50%'
        positions.transform = 'translateX(-50%)'
        positions.width = '90%'
      }

      if (verticalAdjusted === 'bottom')
        positions.top = `${targetRect.bottom + verticalOffset}px`

      if (verticalAdjusted === 'top')
        positions.bottom = `${
          window.innerHeight - targetRect.top + verticalOffset
        }px`

      if (!visible) target.classList.remove('forced-block')

      return positions
    },
    /**
     * Calculates the desired position based on the provided coordinates. For now this
     * is only used by the row context menu, but because of the reserved space of the
     * grid on the right and bottom there is always room for the context. Therefore we
     * do not need to check if the context fits.
     */
    calculatePositionFixed(
      coordinates,
      vertical,
      horizontal,
      verticalOffset,
      horizontalOffset
    ) {
      const targetTop = coordinates.top
      const targetLeft = coordinates.left
      const targetBottom = window.innerHeight - targetTop
      const targetRight = window.innerWidth - targetLeft

      const contextRect = this.$el.getBoundingClientRect()
      const positions = { top: null, right: null, bottom: null, left: null }

      // Take into account that the document might be scrollable.
      verticalOffset += document.documentElement.scrollTop
      horizontalOffset += document.documentElement.scrollLeft

      const { vertical: verticalAdjusted, horizontal: horizontalAdjusted } =
        this.checkForEdges(
          {
            top: targetTop,
            left: targetLeft,
            bottom: targetBottom,
            right: targetRight,
          },
          vertical,
          horizontal,
          verticalOffset,
          horizontalOffset
        )

      // Calculate the correct positions for horizontal and vertical values.
      if (horizontalAdjusted === 'left') {
        positions.transform = 'none'
        positions.left = `${
          targetLeft - contextRect.width + horizontalOffset
        }px`
      }

      if (horizontalAdjusted === 'right') {
        positions.transform = 'none'
        positions.right = `${
          window.innerWidth - targetLeft - contextRect.width - horizontalOffset
        }px`
      }

      if (verticalAdjusted === 'bottom')
        positions.top = `${targetTop + verticalOffset}px`

      if (verticalAdjusted === 'top')
        positions.bottom = `${
          window.innerHeight - targetTop + verticalOffset
        }px`

      return positions
    },
    /**
     * Checks if we need to adjust the horizontal/vertical value of where the context
     * menu will be placed. This might happen if the screen size would cause the context
     * to clip out of the screen if positioned in a certain position.
     *
     * @returns {{horizontal: string, vertical: string}}
     */
    checkForEdges(
      targetRect,
      vertical,
      horizontal,
      verticalOffset,
      horizontalOffset
    ) {
      const contextRect = this.$el.getBoundingClientRect()

      const contextFullHeight =
        (this.$refs.header?.scrollHeight || 0) +
        (this.$refs.mainContainer?.scrollHeight || 0) +
        (this.$refs.footer?.scrollHeight || 0) +
        this.viewportVerticalOffset +
        25 // adding 5 to avoid scrollbar to appear briefly when resizing the window

      const topSpace = targetRect.top - contextFullHeight - verticalOffset

      const canTop = topSpace > 0

      const bottomSpace =
        window.innerHeight - targetRect.top - contextFullHeight - verticalOffset

      const canBottom = bottomSpace > 0

      const canRight =
        targetRect.right - contextRect.width - horizontalOffset > 0

      const canLeft =
        window.innerWidth -
          targetRect.right -
          contextRect.width -
          horizontalOffset >
        0

      // If bottom, top, left or right doesn't fit, but their opposite does we switch to
      // that.
      if (vertical === 'bottom' && !canBottom && canTop) vertical = 'top'

      if (vertical === 'top' && !canTop) vertical = 'bottom'

      if (horizontal === 'left' && !canLeft && canRight) horizontal = 'right'

      if (horizontal === 'right' && !canRight) horizontal = 'left'

      if (!canLeft && !canRight) horizontal = 'window'

      // If both top and bottom don't fit, we check which one has the most space,
      if (!canTop && !canBottom) {
        switch (topSpace > bottomSpace) {
          case true:
            vertical = 'top'
            break
          case false:
            vertical = 'bottom'
            break
          default:
            vertical = 'bottom'
            break
        }
      }

      return { vertical, horizontal }
    },
    setMaxHeight(direction = 'bottom') {
      const element = this.$el
      const elementRect = element.getBoundingClientRect()
      if (direction === 'bottom') {
        const maxHeight =
          window.innerHeight - elementRect.top - this.viewportVerticalOffset
        element.style.maxHeight = `${maxHeight}px`
      } else if (direction === 'top') {
        const maxHeight = elementRect.bottom - this.viewportVerticalOffset
        element.style.maxHeight = `${maxHeight}px`
      }
    },
    isContentScrollable() {
      return (
        this.$refs.mainContainer.scrollHeight >
        this.$refs.mainContainer.clientHeight
      )
    },
    toggleScroll() {
      // disable scroll
      if (this.overflowY === 'auto') {
        switch (this.isScrollable) {
          case true:
            this.overflowY = 'hidden'
            break
          default:
            this.overflowY = 'visible'
            break
        }
      } else {
        // enable scroll
        this.overflowY = 'auto'
      }
    },
    getContainerElement() {
      return this.$refs.mainContainer
    },
    updatePosition(
      target,
      vertical,
      horizontal,
      verticalOffset,
      horizontalOffset
    ) {
      const isElementOrigin = isDomElement(target)
      const css = isElementOrigin
        ? this.calculatePositionElement(
            target,
            vertical,
            horizontal,
            verticalOffset,
            horizontalOffset
          )
        : this.calculatePositionFixed(
            target,
            vertical,
            horizontal,
            verticalOffset,
            horizontalOffset
          )
      // Set the calculated positions of the context.
      for (const key in css) {
        let value = null
        if (typeof css[key] === 'number') value = Math.ceil(css[key]) + 'px'
        else value = css[key] !== null ? css[key] : 'auto'

        this.$el.style[key] = value
      }
      this.updatedOnce = true

      const verticalDirection = css.top ? 'bottom' : 'top'
      this.setMaxHeight(verticalDirection)
    },
  },
}
</script>
