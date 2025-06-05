import { useEffect } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'

export default function AuthSuccessPage({ setIsAuthenticated }) {
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()

  // ставим данные пользователя из гугла в локальное хранилище
  useEffect(() => {
    const sub = searchParams.get('sub')
    const name = searchParams.get('name')
    const redirect = searchParams.get('redirect') || '/competitions'

    if (sub && name) {
      localStorage.setItem('user_id', sub)
      localStorage.setItem('username', name)
      setIsAuthenticated(true)
      navigate(redirect)
    } else {
      // если что-то не то, сразу на повторную авторизацию редирект
      navigate('/login-error')
    }
  }, [navigate, searchParams, setIsAuthenticated])

  return <div>Processing authentication...</div>
}