import { useEffect, useMemo, useState } from 'react'
import {
  ContributionCalendarResponse,
  fetchContributionCalendar,
  fetchGlobalStreak,
} from '../services/domainService'

type StreakData = {
  current: number
  max: number
  last_active_date: string | null
}

const dayToIntensity = (count: number) => {
  if (count >= 10) return 'bg-green-700'
  if (count >= 5) return 'bg-green-600'
  if (count >= 2) return 'bg-green-500'
  if (count >= 1) return 'bg-green-300'
  return 'bg-gray-200'
}

const GlobalStreak = () => {
  const [streak, setStreak] = useState<StreakData | null>(null)
  const [calendar, setCalendar] = useState<
    ContributionCalendarResponse['calendar']
  >([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let mounted = true
    ;(async () => {
      try {
        setLoading(true)
        const [s, c] = await Promise.all([
          fetchGlobalStreak(),
          fetchContributionCalendar(180),
        ])
        if (!mounted) return
        setStreak(s.streak)
        setCalendar(c.calendar)
      } catch (e: unknown) {
        const message = e instanceof Error ? e.message : 'Failed to load streak'
        setError(message)
      } finally {
        setLoading(false)
      }
    })()
    return () => {
      mounted = false
    }
  }, [])

  const weeks = useMemo(() => {
    const cells = calendar.map((d) => ({ date: d.date, count: d.count }))
    const chunks: Array<typeof cells> = []
    for (let i = 0; i < cells.length; i += 7) {
      chunks.push(cells.slice(i, i + 7))
    }
    return chunks
  }, [calendar])

  return (
    <div className="bg-white rounded-lg shadow-md p-4">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold">🔥 Global Streak</h3>
        {streak && (
          <div className="flex items-center space-x-4 text-sm">
            <span>
              Current: <b>{streak.current}</b> days
            </span>
            <span>
              Max: <b>{streak.max}</b> days
            </span>
            <span>
              Last: <b>{streak.last_active_date || '—'}</b>
            </span>
          </div>
        )}
      </div>

      {loading && <div className="text-gray-500">Loading…</div>}
      {error && <div className="text-red-500">{error}</div>}

      {!loading && !error && (
        <div className="overflow-x-auto">
          <div className="flex space-x-1">
            {weeks.map((week, wi) => (
              <div key={wi} className="flex flex-col space-y-1">
                {week.map((cell, di) => (
                  <div
                    key={di}
                    className={`w-3 h-3 rounded-sm ${dayToIntensity(cell.count)}`}
                    title={`${cell.date}: ${cell.count}`}
                  />
                ))}
              </div>
            ))}
          </div>
          <div className="text-xs text-gray-500 mt-2">Last 180 days</div>
        </div>
      )}
    </div>
  )
}

export default GlobalStreak


