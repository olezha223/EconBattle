import { formatDistanceToNow } from 'date-fns'
import { ru } from 'date-fns/locale'

export function formatTimeAgo(date) {
  return formatDistanceToNow(date, {
    addSuffix: true,
    locale: ru
  })
}