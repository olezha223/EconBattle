FROM node:20-alpine

WORKDIR /app

# 1. Копируем файлы зависимостей
COPY package*.json ./

# 2. Устанавливаем зависимости
RUN npm install

# 3. Копируем ВСЕ файлы проекта
COPY . .

# 4. Собираем приложение
RUN npm run build

# 5. Устанавливаем serve глобально
RUN npm install -g serve

# 6. Указываем порт, который будем использовать
EXPOSE 5173

# 7. Запускаем сервер
CMD ["serve", "-s", "dist", "-l", "5173", "--single"]