import { Navigate, useLocation } from 'react-router-dom';

const ProtectedRoute = ({ isAuthenticated, children }) => {
  const location = useLocation();

  if (!isAuthenticated) {
    // Сохраняем текущий путь для редиректа после входа
    return <Navigate to={`/?redirect=${encodeURIComponent(location.pathname)}`} replace />;
  }
  return children;
};

export default ProtectedRoute;