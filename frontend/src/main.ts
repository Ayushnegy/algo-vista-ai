import React from 'react'
import ReactDOM from 'react-dom/client'

import App from './App'
import './aars.css'

const rootEl = document.getElementById('app')
if (!rootEl) throw new Error('Root element #app not found')

const root = ReactDOM.createRoot(rootEl)
root.render(React.createElement(React.StrictMode, null, React.createElement(App)))
