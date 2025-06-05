import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import UserProfile from "../../components/UserProfile/UserProfile.jsx";
import {fetchUserInfo} from "../../services/api.js";


// компонент для страницы пользователя (не текущего)
const UserPage = () => {
  const { userId } = useParams();
  const [userData, setUserData] = useState(null);
  const [loading, setLoading] = useState(true);

  // загрузка данных
  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const data = await fetchUserInfo(userId);
        setUserData(data);
      } catch (error) {
        console.error('Ошибка загрузки данных:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchUserData();
  }, [userId]);

  if (loading) return <div>Загрузка...</div>;
  if (!userData) return <div>Пользователь не найден</div>;

  return <UserProfile userData={userData} />;
};

export default UserPage;