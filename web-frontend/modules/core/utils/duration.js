export const isValidDuration = (inputValue) => {
  if (typeof inputValue === 'number') {
    return true
  } else if (!inputValue) {
    return false
  }
  return guessDurationValueFromString(inputValue) !== null
}

export const roundDurationValueToFormat = (value, format) => {
  if (format === 'h:mm') {
    return Math.round(value / 60) * 60
  } else if (format === 'h:mm:ss') {
    return Math.round(value)
  } else if (format === 'h:mm:ss.s') {
    return Math.round(value * 10) / 10
  } else if (format === 'h:mm:ss.ss') {
    return Math.round(value * 100) / 100
  } else if (format === 'h:mm:ss.sss') {
    return Math.round(value * 1000) / 1000
  }
  return value
}

export const guessDurationValueFromString = (inputValue) => {
  const tokens = inputValue.split(':').reverse()

  const hasSeconds = tokens.length > 2
  const multipliers = hasSeconds ? [1, 60, 3600] : [60, 3600]

  const duration = tokens.reduce((acc, token, index) => {
    const number = parseFloat(token)

    if (isNaN(number)) {
      return null
    }

    const multiplier = multipliers[index]
    return acc + number * multiplier
  }, 0)

  return duration
}

export const AVAILABLE_DURATION_FORMATS = [
  'h:mm',
  'h:mm:ss',
  'h:mm:ss.s',
  'h:mm:ss.ss',
  'h:mm:ss.sss',
]

export const DURATION_FORMATS_OPTIONS = {
  'h:mm': {
    toString(hours, minutes) {
      return `${hours}:${minutes.toString().padStart(2, '0')}`
    },
  },
  'h:mm:ss': {
    toString(hours, minutes, seconds) {
      return `${hours}:${minutes.toString().padStart(2, '0')}:${seconds
        .toString()
        .padStart(2, '0')}`
    },
  },
  'h:mm:ss.s': {
    toString(hours, minutes, seconds) {
      return `${hours}:${minutes.toString().padStart(2, '0')}:${seconds
        .toFixed(1)
        .padStart(4, '0')}`
    },
  },
  'h:mm:ss.ss': {
    toString(hours, minutes, seconds) {
      return `${hours}:${minutes.toString().padStart(2, '0')}:${seconds
        .toFixed(2)
        .padStart(5, '0')}`
    },
  },
  'h:mm:ss.sss': {
    toString(hours, minutes, seconds) {
      return `${hours}:${minutes.toString().padStart(2, '0')}:${seconds
        .toFixed(3)
        .padStart(6, '0')}`
    },
  },
}

export const formatDuration = (value, durationFormat) => {
  if (value === null) {
    return ''
  }

  const hours = Math.floor(value / 3600)
  const mins = Math.floor((value - hours * 3600) / 60)
  const secs = value - hours * 3600 - mins * 60
  return DURATION_FORMATS_OPTIONS[durationFormat].toString(hours, mins, secs)
}
