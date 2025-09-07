import { useEffect, useMemo, useState } from 'react';
import {
  ContributionCalendarResponse,
  fetchContributionCalendar,
  fetchGlobalStreak,
} from '../services/domainService';

type StreakData = {
  current: number;
  max: number;
  last_active_date: string | null;
};

const dayToIntensity = (count: number) => {
  if (count >= 10) return 'bg-green-700';
  if (count >= 5) return 'bg-green-600';
  if (count >= 2) return 'bg-green-500';
  if (count >= 1) return 'bg-green-300';
  return 'bg-gray-200';
};

const GlobalStreak = () => {
  const [streak, setStreak] = useState<StreakData | null>(null);
  const [calendar, setCalendar] = useState<
    ContributionCalendarResponse['calendar']
  >([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [year, setYear] = useState<number>(new Date().getFullYear());

  useEffect(() => {
    let mounted = true;
    (async () => {
      try {
        setLoading(true);
        const [s, c] = await Promise.all([
          fetchGlobalStreak(),
          fetchContributionCalendar(180),
        ]);
        if (!mounted) return;
        setStreak(s.streak);
        setCalendar(c.calendar);
      } catch (e: unknown) {
        const message = e instanceof Error ? e.message : 'Failed to load streak';
        setError(message);
      } finally {
        setLoading(false);
      }
    })();
    return () => {
      mounted = false;
    };
  }, []);

  // Build a year grid similar to GitHub contributions
  const { weeks, monthLabels } = useMemo(() => {
    const start = new Date(year, 0, 1);
    const end = new Date(year, 11, 31);

    // Start from the Monday of the first week (for nice alignment)
    const dayOfWeek = (start.getDay() + 6) % 7; // convert Sun(0)→6, Mon(1)→0
    const gridStart = new Date(start);
    gridStart.setDate(start.getDate() - dayOfWeek);

    // Index calendar by date string
    const map = new Map<string, number>();
    for (const item of calendar) {
      map.set(item.date, item.count);
    }

    const weeksArr: Array<Array<{ date: string; count: number; inYear: boolean }>> = [];
    const months: string[] = [];

    let cursor = new Date(gridStart);
    while (cursor <= end || cursor.getDay() !== 0) {
      // Build one column (week)
      const col: Array<{ date: string; count: number; inYear: boolean }> = [];
      for (let i = 0; i < 7; i++) {
        const iso = cursor.toISOString().slice(0, 10);
        const inYear = cursor.getFullYear() === year;
        col.push({ date: iso, count: map.get(iso) || 0, inYear });
        cursor.setDate(cursor.getDate() + 1);
      }
      // Month label at first day-of-month inside the year
      const firstInYear = col.find((c) => c.inYear);
      if (firstInYear) {
        const dt = new Date(firstInYear.date);
        const label = dt.toLocaleString('default', { month: 'short' });
        if (months.length === 0 || months[months.length - 1] !== label) {
          months.push(label);
        } else {
          months.push('');
        }
      } else {
        months.push('');
      }
      weeksArr.push(col);
      // Stop when we have passed the end of year and completed the last week column fully outside the year
      if (cursor > end && weeksArr[weeksArr.length - 1].every((c) => !c.inYear)) break;
    }

    return { weeks: weeksArr, monthLabels: months };
  }, [calendar, year]);

  return (
    <div className="bg-white rounded-lg shadow-md p-4">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold">Working Streak</h3>
        <div className="flex items-center space-x-4">
          <button
            className="px-2 py-1 text-gray-600 hover:text-gray-900"
            onClick={() => setYear((y) => y - 1)}
            aria-label="Previous year"
          >
            ‹
          </button>
          <div className="font-semibold">{year}</div>
          <button
            className="px-2 py-1 text-gray-600 hover:text-gray-900"
            onClick={() => setYear((y) => y + 1)}
            aria-label="Next year"
          >
            ›
          </button>
        </div>
      </div>

      {loading && <div className="text-gray-500">Loading…</div>}
      {error && <div className="text-red-500">{error}</div>}

      {!loading && !error && (
        <div className="overflow-x-auto">
          {/* Months header */}
          <div className="flex ml-10 mb-1 text-xs text-gray-500 select-none">
            {monthLabels.map((m, i) => (
              <div key={i} className="w-4 text-center">
                {m}
              </div>
            ))}
          </div>

          <div className="flex">
            {/* Weekday labels */}
            <div className="mr-2 text-xs text-gray-500 select-none">
              <div className="h-4" />
              <div className="h-4">Mon</div>
              <div className="h-4" />
              <div className="h-4">Wed</div>
              <div className="h-4" />
              <div className="h-4">Fri</div>
              <div className="h-4" />
              <div className="h-4">Sun</div>
            </div>

            {/* Grid */}
            <div className="flex space-x-1">
              {weeks.map((week, wi) => (
                <div key={wi} className="flex flex-col space-y-1">
                  {week.map((cell, di) => (
                    <div
                      key={di}
                      className={`w-3 h-3 rounded ${cell.inYear ? dayToIntensity(cell.count) : 'bg-transparent'}`}
                      title={`${cell.date}: ${cell.count}`}
                    />
                  ))}
                </div>
              ))}
            </div>
          </div>

          {/* Legend */}
          <div className="flex items-center justify-end mt-3 text-xs text-gray-600">
            <span className="mr-2">Less</span>
            <span className="w-3 h-3 rounded bg-gray-200 mr-1" />
            <span className="w-3 h-3 rounded bg-green-300 mr-1" />
            <span className="w-3 h-3 rounded bg-green-500 mr-1" />
            <span className="w-3 h-3 rounded bg-green-700 mr-2" />
            <span>More</span>
          </div>
        </div>
      )}

      {/* Stats footer */}
      {streak && (
        <div className="mt-4 flex items-center justify-between text-sm">
          <div>
            Current streak: <span className="text-green-600 font-semibold">{streak.current} days</span>
          </div>
          <div>
            Longest streak: <span className="text-orange-600 font-semibold">{streak.max} days</span>
          </div>
        </div>
      )}
    </div>
  );
};

export default GlobalStreak;


