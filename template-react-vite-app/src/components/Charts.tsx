import { Task } from '../store/slices/taskSlice';
import { Tag } from '../store/slices/tagSlice';
import { Bar, Pie } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
} from 'chart.js';
import { useState } from 'react';
import { TooltipItem } from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
);

interface ExperienceAnalyticsProps {
  tasks: Task[];
  tags: Record<string, Tag>;
}

type TimeRange = 'daily' | 'monthly' | 'yearly';

const ExperienceAnalytics = ({ tasks, tags }: ExperienceAnalyticsProps) => {
  const [timeRange, setTimeRange] = useState<TimeRange>('daily');
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  const [selectedDate, setSelectedDate] = useState<Date>(today);

  const handleDateChange = (date: Date) => {
    const newDate = new Date(date);
    newDate.setHours(0, 0, 0, 0);
    setSelectedDate(newDate);
  };

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('vi-VN', {
      style: 'currency',
      currency: 'VND',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(value);
  };

  const formatDate = (date: Date, range: TimeRange) => {
    const day = date.getDate();
    const month = date.getMonth() + 1;
    const year = date.getFullYear();

    switch (range) {
      case 'daily':
        return `${day}/${month}`;
      case 'monthly':
        return `Tháng ${month}/${year}`;
      case 'yearly':
        return `Năm ${year}`;
    }
  };

  // Prepare experience data based on time range
  const getExperienceData = (range: TimeRange) => {
    const dates = [];
    const experiences = [];
    const today = selectedDate;
    today.setHours(0, 0, 0, 0);

    switch (range) {
      case 'daily':
        for (let i = 6; i >= 0; i--) {
          const date = new Date(today);
          date.setDate(date.getDate() - i);
          const startOfDay = new Date(
            date.getFullYear(),
            date.getMonth(),
            date.getDate(),
            0,
            0,
            0,
          );
          const endOfDay = new Date(
            date.getFullYear(),
            date.getMonth(),
            date.getDate(),
            23,
            59,
            59,
          );

          const dailyTotal = tasks
            .filter((task) => {
              const taskDate = new Date(task.date);
              return taskDate >= startOfDay && taskDate <= endOfDay;
            })
            .reduce((sum, task) => sum + task.value, 0);

          dates.push(formatDate(date, range));
          experiences.push(dailyTotal);
        }
        break;

      case 'monthly':
        for (let i = 5; i >= 0; i--) {
          const date = new Date(today);
          date.setMonth(date.getMonth() - i);
          const monthStart = new Date(date.getFullYear(), date.getMonth(), 1);
          const monthEnd = new Date(date.getFullYear(), date.getMonth() + 1, 0);
          const monthlyTotal = tasks
            .filter((task) => {
              const taskDate = new Date(task.date);
              return taskDate >= monthStart && taskDate <= monthEnd;
            })
            .reduce((sum, task) => sum + task.value, 0);
          dates.push(formatDate(date, range));
          experiences.push(monthlyTotal);
        }
        break;

      case 'yearly':
        for (let i = 4; i >= 0; i--) {
          const date = new Date(today);
          date.setFullYear(date.getFullYear() - i);
          const yearStart = new Date(date.getFullYear(), 0, 1);
          const yearEnd = new Date(date.getFullYear(), 11, 31);
          const yearlyTotal = tasks
            .filter((task) => {
              const taskDate = new Date(task.date);
              return taskDate >= yearStart && taskDate <= yearEnd;
            })
            .reduce((sum, task) => sum + task.value, 0);
          dates.push(formatDate(date, range));
          experiences.push(yearlyTotal);
        }
        break;
    }

    return { dates, experiences };
  };

  // Prepare tag distribution data based on time range
  const getTagDistributionData = (range: TimeRange) => {
    const today = selectedDate;
    today.setHours(0, 0, 0, 0);
    const startDate = new Date(today);

    switch (range) {
      case 'daily':
        startDate.setDate(today.getDate() - 6);
        break;
      case 'monthly':
        startDate.setMonth(today.getMonth() - 5);
        break;
      case 'yearly':
        startDate.setFullYear(today.getFullYear() - 4);
        break;
    }

    console.log('Selected Date Range:', { startDate, endDate: today });

    // Initialize tagValues with all available tags
    const tagValues: Record<string, number> = {};
    Object.keys(tags).forEach((tag) => {
      tagValues[tag] = tags[tag].xp || 0;
    });

    console.log('Initial Tag Values:', tagValues);

    // Add values from filtered tasks
    const filteredTasks = tasks.filter((task) => {
      const taskDate = new Date(task.date);
      return taskDate >= startDate && taskDate <= today;
    });

    console.log('Filtered Tasks:', filteredTasks);

    filteredTasks.forEach((task) => {
      task.tags.forEach((tag) => {
        if (!tagValues[tag]) {
          tagValues[tag] = 0;
        }
        tagValues[tag] += Math.abs(task.value);
      });
    });

    console.log('Final Tag Values:', tagValues);

    const tagLabels = Object.keys(tagValues).filter(
      (tag) => tagValues[tag] > 0,
    );
    const data = {
      labels: tagLabels,
      data: tagLabels.map((tag) => tagValues[tag]),
      colors: tagLabels.map((tag) => {
        // Lấy màu từ thuộc tính color của tag trong store
        const baseColor = tags[tag]?.color || '#6B7280'; // Màu xám mặc định nếu không có màu
        return {
          backgroundColor: `${baseColor}CC`,
          borderColor: baseColor,
        };
      }),
    };

    console.log('Pie Chart Data:', data);
    return data;
  };

  const { dates, experiences } = getExperienceData(timeRange);
  const tagData = getTagDistributionData(timeRange);

  const experienceData = {
    labels: dates,
    datasets: [
      {
        label: 'Kinh nghiệm (KINH NGHIỆM)',
        data: experiences,
        backgroundColor: experiences.map((value) =>
          value >= 0 ? 'rgba(72, 187, 120, 0.7)' : 'rgba(229, 62, 62, 0.7)',
        ),
        borderColor: experiences.map((value) =>
          value >= 0 ? 'rgb(47, 133, 90)' : 'rgb(197, 48, 48)',
        ),
        borderWidth: 1,
      },
    ],
  };

  const tagDistributionData = {
    labels: tagData.labels,
    datasets: [
      {
        data: tagData.data,
        backgroundColor: tagData.colors.map((color) => color.backgroundColor),
        borderColor: tagData.colors.map((color) => color.borderColor),
        borderWidth: 2,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      y: {
        type: 'linear' as const,
        beginAtZero: true,
        grace: '5%',
        ticks: {
          callback: function (
            this: /* Chart.js Tick */ any,
            tickValue: string | number,
          ) {
            return `${tickValue} XP`;
          },
        },
      },
    },
    plugins: {
      tooltip: {
        callbacks: {
          label: function (
            this: /* Chart.js Tooltip */ any,
            tooltipItem: TooltipItem<any>,
          ) {
            return `${tooltipItem.raw} XP`;
          },
        },
      },
    },
  };

  const pieOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      tooltip: {
        callbacks: {
          label: (context: TooltipItem<any>) => {
            const label = context.label || '';
            const value = context.raw as number;
            const total = context.dataset.data.reduce(
              (a: number, b: number) => a + b,
              0,
            );
            const percentage = Math.round((value / total) * 100);
            return `${label}: ${formatCurrency(value)} (${percentage}%)`;
          },
        },
      },
      legend: {
        display: true,
        position: 'bottom' as const,
      },
    },
  };

  return (
    <div className="mt-8 grid grid-cols-1 lg:grid-cols-2 gap-6">
      <div className="bg-white p-6 rounded-lg shadow-md">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-semibold text-gray-800">
            Kinh Nghiệm Theo Thời Gian
          </h2>
          <div className="flex items-center space-x-4">
            <input
              type="date"
              value={selectedDate.toISOString().split('T')[0]}
              onChange={(e) => handleDateChange(new Date(e.target.value))}
              className="px-3 py-1 border rounded"
            />
            <div className="flex space-x-2">
              <button
                onClick={() => setTimeRange('daily')}
                className={`px-3 py-1 rounded ${
                  timeRange === 'daily'
                    ? 'bg-indigo-600 text-white'
                    : 'bg-gray-200 text-gray-700'
                }`}
              >
                Ngày
              </button>
              <button
                onClick={() => setTimeRange('monthly')}
                className={`px-3 py-1 rounded ${
                  timeRange === 'monthly'
                    ? 'bg-indigo-600 text-white'
                    : 'bg-gray-200 text-gray-700'
                }`}
              >
                Tháng
              </button>
              <button
                onClick={() => setTimeRange('yearly')}
                className={`px-3 py-1 rounded ${
                  timeRange === 'yearly'
                    ? 'bg-indigo-600 text-white'
                    : 'bg-gray-200 text-gray-700'
                }`}
              >
                Năm
              </button>
            </div>
          </div>
        </div>
        <div className="chart-container" style={{ height: '300px' }}>
          <Bar data={experienceData} options={chartOptions} />
        </div>
      </div>

      <div className="bg-white p-6 rounded-lg shadow-md">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-semibold text-gray-800">
            Phân Bố Theo Tag
          </h2>
          <div className="flex space-x-2">
            <button
              onClick={() => setTimeRange('daily')}
              className={`px-3 py-1 rounded ${
                timeRange === 'daily'
                  ? 'bg-indigo-600 text-white'
                  : 'bg-gray-200 text-gray-700'
              }`}
            >
              Ngày
            </button>
            <button
              onClick={() => setTimeRange('monthly')}
              className={`px-3 py-1 rounded ${
                timeRange === 'monthly'
                  ? 'bg-indigo-600 text-white'
                  : 'bg-gray-200 text-gray-700'
              }`}
            >
              Tháng
            </button>
            <button
              onClick={() => setTimeRange('yearly')}
              className={`px-3 py-1 rounded ${
                timeRange === 'yearly'
                  ? 'bg-indigo-600 text-white'
                  : 'bg-gray-200 text-gray-700'
              }`}
            >
              Năm
            </button>
          </div>
        </div>
        <div className="chart-container" style={{ height: '300px' }}>
          {tagData.labels.length === 0 ? (
            <div className="flex items-center justify-center h-full text-gray-500">
              Không có dữ liệu
            </div>
          ) : (
            <Pie data={tagDistributionData} options={pieOptions} />
          )}
        </div>
      </div>
    </div>
  );
};

export default ExperienceAnalytics;
