import styles from './ActivityGrid.module.css';

export default function ActivityGrid({ userActivity }) {
  if (!userActivity) return null;

  // Получаем и сортируем все даты
  const dates = Object.keys(userActivity)
    .sort((a, b) => new Date(a) - new Date(b));

  // Создаем матрицу недель
  const weeks = [];
  let currentWeek = [];

  dates.forEach(date => {
    const day = new Date(date).getDay(); // 0-6 (воскресенье-суббота)
    const adjustedDay = day === 0 ? 6 : day - 1; // преобразуем к 0-6 (понедельник-воскресенье)

    if (adjustedDay === 0 && currentWeek.length > 0) {
      weeks.push(currentWeek);
      currentWeek = [];
    }

    currentWeek[adjustedDay] = {
      date,
      activity: userActivity[date]
    };
  });

  if (currentWeek.length > 0) weeks.push(currentWeek);

  // Находим максимальную активность для цветов
  const maxActivity = Math.max(...Object.values(userActivity));

  return (
    <div className={styles.activityContainer}>
      {/* Легенда дней недели */}
      <div className={styles.weekDaysLegend}>
        {['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'].map((day, index) => (
          <div key={index} className={styles.weekDay}>{day}</div>
        ))}
      </div>

      {/* Сетка активности */}
      <div className={styles.weeksGrid}>
        {weeks.map((week, weekIndex) => (
          <div key={weekIndex} className={styles.weekColumn}>
            {Array(7).fill().map((_, dayIndex) => {
              const dayData = week[dayIndex];
              const activity = dayData?.activity || 0;
              const intensity = activity > 0 ? activity / maxActivity : 0;

              return (
                <div
                  key={dayIndex}
                  className={styles.dayCell}
                  data-tooltip={dayData ?
                    `${new Date(dayData.date).toLocaleDateString('ru-RU')}: ${activity} активностей` :
                    'Нет данных'}
                >
                  <div
                    className={styles.activitySquare}
                    style={{
                      backgroundColor: activity > 0
                        ? `rgba(46, 160, 67, ${0.2 + intensity * 0.8})`
                        : '#ebedf0'
                    }}
                  />
                </div>
              );
            })}
          </div>
        ))}
      </div>
    </div>
  );
}
