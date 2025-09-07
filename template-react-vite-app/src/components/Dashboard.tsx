import { Task } from '../store/slices/taskSlice';
import { Tag } from '../store/slices/tagSlice';

interface ExperienceOverviewProps {
  tasks: Task[];
  tags: Record<string, Tag>;
}

const ExperienceOverview = ({ tasks, tags }: ExperienceOverviewProps) => {
  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('vi-VN', {
      style: 'currency',
      currency: 'VND',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(value);
  };

  // Calculate totals
  const totalIncome = tasks
    .filter((task) => task.value > 0)
    .reduce((sum, task) => sum + task.value, 0);
  const totalExpense = tasks
    .filter((task) => task.value < 0)
    .reduce((sum, task) => sum + task.value, 0);
  const netBalance = totalIncome + totalExpense;

  // Calculate top tags
  const tagStats: Record<
    string,
    { totalValue: number; taskCount: number; streakDays: number }
  > = {};

  tasks.forEach((task) => {
    task.tags.forEach((tag) => {
      if (!tagStats[tag]) {
        tagStats[tag] = {
          totalValue: 0,
          taskCount: 0,
          streakDays: tags[tag]?.streakDays || 0,
        };
      }

      tagStats[tag].totalValue += task.value;
      tagStats[tag].taskCount += 1;
    });
  });

  const topTags = Object.keys(tagStats)
    .sort((a, b) => tagStats[b].taskCount - tagStats[a].taskCount)
    .slice(0, 3);

  return (
    <div className="mt-8 bg-white p-6 rounded-lg shadow-md">
      <h2 className="text-xl font-semibold text-gray-800 mb-4">
        Tổng Quan Kinh Nghiệm
      </h2>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-green-50 p-4 rounded-lg border border-green-200">
          <h3 className="text-sm font-medium text-green-700">
            Tổng Kinh Nghiệm Tích Lũy
          </h3>
          <p className="text-2xl font-bold text-green-600 mt-1">
            {formatCurrency(totalIncome)}
          </p>
        </div>

        <div className="bg-red-50 p-4 rounded-lg border border-red-200">
          <h3 className="text-sm font-medium text-red-700">
            Tổng Kinh Nghiệm Tiêu Hao
          </h3>
          <p className="text-2xl font-bold text-red-600 mt-1">
            {formatCurrency(totalExpense)}
          </p>
        </div>

        <div className="bg-blue-50 p-4 rounded-lg border border-blue-200">
          <h3 className="text-sm font-medium text-blue-700">
            Kinh Nghiệm Còn Lại
          </h3>
          <p className="text-2xl font-bold text-blue-600 mt-1">
            {formatCurrency(netBalance)}
          </p>
        </div>
      </div>

      <div className="mt-6">
        <h3 className="text-lg font-medium text-gray-800 mb-3">
          Tag Hoạt Động Nhiều Nhất
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {topTags.length === 0 ? (
            <div className="col-span-full text-center py-4 text-gray-500">
              Chưa có dữ liệu.
            </div>
          ) : (
            topTags.map((tagName) => {
              const stats = tagStats[tagName];
              return (
                <div
                  key={tagName}
                  className="bg-gray-50 p-4 rounded-lg border-l-4"
                  style={{
                    borderLeftColor: tags[tagName]
                      ? tags[tagName].color
                      : '#CBD5E0',
                  }}
                >
                  <div className="flex justify-between items-center">
                    <span
                      className="tag-pill"
                      style={{
                        backgroundColor: tags[tagName]
                          ? `${tags[tagName].color}33`
                          : '#CBD5E033',
                        color: tags[tagName] ? tags[tagName].color : '#718096',
                      }}
                    >
                      {tagName}
                    </span>
                    <span className="text-sm font-medium">
                      {stats.taskCount} task
                    </span>
                  </div>
                  <div
                    className={`mt-2 ${stats.totalValue >= 0 ? 'text-green-600' : 'text-red-600'} font-bold`}
                  >
                    {formatCurrency(stats.totalValue)}
                  </div>
                  <div className="mt-1 text-xs text-gray-500">
                    Level {tags[tagName] ? tags[tagName].level : 0} • Streak{' '}
                    {stats.streakDays} ngày
                    {tags[tagName]?.maxStreakDays && tags[tagName].maxStreakDays > stats.streakDays && (
                      <span className="text-gray-400"> (Max: {tags[tagName].maxStreakDays})</span>
                    )}
                  </div>
                </div>
              );
            })
          )}
        </div>
      </div>
    </div>
  );
};

export default ExperienceOverview;
