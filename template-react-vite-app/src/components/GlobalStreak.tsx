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

// Sizing controls
const CELL_SIZE = 14; // px (increase to make bigger)
const CELL_GAP = 3; // px
const FONT_SM = 'text-sm';
const LABEL_COL_WIDTH = 48; // px for weekday labels column

const dayToColor = (count: number) => {
  if (count >= 10) return '#166534'; // green-800
  if (count >= 5) return '#15803d'; // green-700
  if (count >= 2) return '#16a34a'; // green-600
  if (count >= 1) return '#86efac'; // green-300
  return '#e5e7eb'; // gray-200
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
          fetchContributionCalendar(366),
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

  const { weeks, monthSegments } = useMemo(() => {
    const start = new Date(year, 0, 1);
    const end = new Date(year, 11, 31);
    const dayOfWeek = (start.getDay() + 6) % 7; // Monday=0
    const gridStart = new Date(start);
    gridStart.setDate(start.getDate() - dayOfWeek);

    const map = new Map<string, number>();
    for (const item of calendar) map.set(item.date, item.count);

    const weeksArr: Array<Array<{ date: string; count: number; inYear: boolean }>> = [];
    const monthOfWeek: Array<string | null> = [];

    let cursor = new Date(gridStart);
    while (cursor <= end || cursor.getDay() !== 0) {
      const col: Array<{ date: string; count: number; inYear: boolean }> = [];
      for (let i = 0; i < 7; i++) {
        const iso = cursor.toISOString().slice(0, 10);
        const inYear = cursor.getFullYear() === year;
        col.push({ date: iso, count: map.get(iso) || 0, inYear });
        cursor.setDate(cursor.getDate() + 1);
      }
      const rep = col.find((c, idx) => c.inYear && idx === 3) || col.find((c) => c.inYear);
      if (rep) {
        const dt = new Date(rep.date);
        const label = dt.toLocaleString('default', { month: 'short' });
        monthOfWeek.push(label);
      } else {
        monthOfWeek.push(null);
      }
      weeksArr.push(col);
      if (cursor > end && weeksArr[weeksArr.length - 1].every((c) => !c.inYear)) break;
    }
    const segments: Array<{ label: string; span: number }> = [];
    for (let i = 0; i < monthOfWeek.length; i++) {
      const label = monthOfWeek[i];
      if (!label) continue;
      if (segments.length === 0 || segments[segments.length - 1].label !== label) {
        segments.push({ label, span: 1 });
      } else {
        segments[segments.length - 1].span += 1;
      }
    }
    return { weeks: weeksArr, monthSegments: segments };
  }, [calendar, year]);

  return (
    <div className="bg-white rounded-lg shadow-md p-5">
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
          {/* Month header - spans equal to number of week columns in month */}
          <div
            className={`flex mb-2 ${FONT_SM} text-gray-600 select-none`}
            style={{ marginLeft: LABEL_COL_WIDTH }}
          >
            {monthSegments.map((seg, i) => (
              <div
                key={`${seg.label}-${i}`}
                className="text-center"
                style={{ width: seg.span * (CELL_SIZE + CELL_GAP) }}
              >
                {seg.label}
              </div>
            ))}
          </div>

          <div className="flex">
            {/* Weekday labels */}
            <div
              className={`mr-3 ${FONT_SM} text-gray-600 select-none`}
              style={{ lineHeight: `${CELL_SIZE + CELL_GAP}px`, width: LABEL_COL_WIDTH }}
            >
              {['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'].map((d) => (
                <div key={d} style={{ height: CELL_SIZE + CELL_GAP }}>{d}</div>
              ))}
            </div>

            {/* Grid */}
            <div style={{ display: 'flex', columnGap: CELL_GAP }}>
              {weeks.map((week, wi) => (
                <div
                  key={wi}
                  style={{ display: 'flex', flexDirection: 'column', rowGap: CELL_GAP }}
                >
                  {week.map((cell, di) => (
                    <div
                      key={di}
                      title={`${cell.date}: ${cell.count}`}
                      style={{
                        width: CELL_SIZE,
                        height: CELL_SIZE,
                        borderRadius: 3,
                        backgroundColor: cell.inYear ? dayToColor(cell.count) : 'transparent',
                      }}
                    />
                  ))}
                </div>
              ))}
            </div>
          </div>

          {/* Legend */}
          <div className={`flex items-center justify-end mt-3 ${FONT_SM} text-gray-600`}>
            <span className="mr-2">Less</span>
            {[0, 1, 3, 6, 10].map((n) => (
              <span
                key={n}
                style={{
                  width: CELL_SIZE,
                  height: CELL_SIZE,
                  borderRadius: 3,
                  backgroundColor: dayToColor(n),
                  marginRight: 4,
                }}
              />
            ))}
            <span>More</span>
          </div>
        </div>
      )}

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


