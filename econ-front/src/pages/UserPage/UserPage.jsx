import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import UserProfile from "../../components/UserProfile/UserProfile.jsx";

const API_URL = 'http://localhost:8000';

const UserPage = () => {
  const { userId } = useParams();
  const [userData, setUserData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const response = await axios.get(
          `${API_URL}/users/info?user_id=${userId}`,
          { withCredentials: true }
        );
        setUserData(response.data);
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