// src/pages/AuthSuccessPage.jsx
import { useEffect } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'

export default function AuthSuccessPage() {
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()

  useEffect(() => {
    const sub = searchParams.get('sub')
    const name = searchParams.get('name')

    if (sub && name) {
      localStorage.setItem('user_id', sub)
      localStorage.setItem('username', name)
      navigate('/competitions')
    } else {
      navigate('/?error=auth_failed')
    }
  }, [navigate, searchParams])

  return <div>Processing authentication...</div>
}