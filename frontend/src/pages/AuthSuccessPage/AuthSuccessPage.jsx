import {useEffect} from "react";
import {useNavigate, useSearchParams} from "react-router-dom";

export default function AuthSuccessPage({ setIsAuthenticated }) {
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()

  useEffect(() => {
    const sub = searchParams.get('sub')
    const name = searchParams.get('name')
    const redirectPath = searchParams.get('redirect') || '/competitions'

    if (sub && name) {
      localStorage.setItem('user_id', sub)
      localStorage.setItem('username', name)
      setIsAuthenticated(true)
      navigate(redirectPath)
    } else {
      navigate('/?error=auth_failed')
    }
  }, [navigate, searchParams, setIsAuthenticated])

  return <div>Processing authentication...</div>
}