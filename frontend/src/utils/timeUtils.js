import { formatDistanceToNow } from 'date-fns'
import { ru } from 'date-fns/locale'

// Возвращает сколько времени назад произошло событие
export function formatTimeAgo(date) {
  return formatDistanceToNow(date, {
    addSuffix: true,
    locale: ru
  })
}