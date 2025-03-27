// hooks/useWebSocket.js
import { useEffect, useRef, useState } from 'react'

export default function useWebSocket(url) {
  const [lastMessage, setLastMessage] = useState(null)
  const wsRef = useRef(null)

  const connect = () => {
    wsRef.current = new WebSocket(url)

    wsRef.current.onopen = () => {
      console.log('WebSocket connected')
    }

    wsRef.current.onmessage = (event) => {
      setLastMessage(event)
    }

    wsRef.current.onclose = (e) => {
      console.log('WebSocket closed:', e.reason)
    }

    wsRef.current.onerror = (error) => {
      console.error('WebSocket error:', error)
    }
  }

  useEffect(() => {
    connect()

    return () => {
      if (wsRef.current?.readyState === WebSocket.OPEN) {
        wsRef.current.close(1000, 'Component unmounted')
      }
    }
  }, [url])

  const sendMessage = (message) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify(message))
    }
  }

  return { sendMessage, lastMessage }
}