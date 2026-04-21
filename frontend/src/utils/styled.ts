// Simple styled helper that returns inline styles
// This is a minimal replacement for BaseUI's styled() which was removed in v10

import React from 'react'

type Styles = Record<string, React.CSSProperties>

export function styled(
  component: string,
  styles: Styles | ((props: any) => Styles)
) {
  return (props: any) => {
    const resolvedStyles = typeof styles === 'function' ? styles(props) : styles
    return React.createElement(component, {
      style: { ...props.style, ...resolvedStyles },
      className: props.className,
    })
  }
}

// For components that don't need dynamic props, return a simple component
export function styledStatic(component: string, styles: Styles) {
  return (props: any) =>
    React.createElement(component, {
      style: { ...props.style, ...styles },
      className: props.className,
    })
}
