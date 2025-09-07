import { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { RootState } from '../store';
import { createSelector } from '@reduxjs/toolkit';
import { addTask, deleteTask, setCurrentDate } from '../store/slices/taskSlice';
import { addTagXP, removeTagXP } from '../store/slices/tagSlice';
import TaskForm from '../components/TaskForm';
import TaskList from '../components/TaskList';
import TagLevels from '../components/TagLevels';
import TreeView from '../components/TreeView';
import Charts from '../components/Charts';
import ExperienceOverview from '../components/ExperienceOverview';
import Notification from '../components/Notification';
import GlobalStreak from '../components/GlobalStreak';

const selectTasks = createSelector(
  (state: RootState) => state.tasks,
  (tasksState) => ({
    tasks: tasksState.tasks,
    currentDate: tasksState.currentDate,
  }),
);

const selectTags = createSelector(
  (state: RootState) => state.tags,
  (tagsState) => tagsState.tags,
);

const TaskManager = () => {
  const dispatch = useDispatch();
  const { tasks, currentDate } = useSelector(selectTasks);
  const tags = useSelector(selectTags);
  const [notifications, setNotifications] = useState<
    Array<{ id: number; message: string; type: string }>
  >([]);

  const handleAddTask = (taskData: {
    name: string;
    tags: string[];
    value: number;
    date: string;
  }) => {
    dispatch(addTask(taskData));
    taskData.tags.forEach((tag) => {
      dispatch(
        addTagXP({
          tagName: tag,
          value: taskData.value,
          date: taskData.date,
        }),
      );
    });
    showNotification('Task đã được thêm thành công', 'success');
  };

  const handleDeleteTask = (taskId: number) => {
    const task = tasks.find((t) => t.id === taskId);
    if (task) {
      dispatch(deleteTask(taskId));
      task.tags.forEach((tag) => {
        dispatch(removeTagXP({ tagName: tag, value: task.value }));
      });
      showNotification('Task đã được xóa', 'info');
    }
  };

  const handleDateChange = (date: string) => {
    dispatch(setCurrentDate(date));
  };

  const showNotification = (message: string, type: string) => {
    const id = Date.now();
    setNotifications((prev) => [...prev, { id, message, type }]);
    setTimeout(() => {
      setNotifications((prev) => prev.filter((n) => n.id !== id));
    }, 3000);
  };

  const [activeTab, setActiveTab] = useState<'overview' | 'tree'>('overview');

  return (
    <div className="space-y-6">
      {/* Top Section: Task Form + Quick Stats */}
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        <div className="lg:col-span-1">
          <div className="min-h-[520px]">{/* Increase TaskForm vertical space */}
            <TaskForm onSubmit={handleAddTask} />
          </div>
        </div>
        <div className="lg:col-span-3">
          {/* Tab Navigation */}
          <div className="bg-white rounded-lg shadow-md">
            <div className="border-b border-gray-200">
              <nav className="flex space-x-8 px-6">
                <button
                  onClick={() => setActiveTab('overview')}
                  className={`py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
                    activeTab === 'overview'
                      ? 'border-blue-500 text-blue-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  📊 Tags Overview
                </button>
                <button
                  onClick={() => setActiveTab('tree')}
                  className={`py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
                    activeTab === 'tree'
                      ? 'border-blue-500 text-blue-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  🌳 Tree Structure
                </button>
              </nav>
            </div>

            {/* Tab Content */}
            <div className={activeTab === 'overview' ? 'p-6' : 'p-0'}>
              {activeTab === 'overview' ? (
                <div className="space-y-6">
                  <GlobalStreak />
                  <TagLevels tags={tags} />
                </div>
              ) : (
                <div className="max-h-[720px] overflow-y-auto">{/* Increase TreeView height */}
                  <TreeView className="shadow-none border-0" />
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Tasks Section */}
      <div className="mt-8">{/* Push TaskList a bit lower */}
        <TaskList
          tasks={tasks}
          currentDate={currentDate}
          onDeleteTask={handleDeleteTask}
          onDateChange={handleDateChange}
        />
      </div>

      {/* Analytics Section */}
      <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
        <Charts tasks={tasks} tags={tags} />
        <ExperienceOverview tasks={tasks} tags={tags} />
      </div>

      {/* Notifications */}
      <div className="fixed bottom-4 right-4 z-50 space-y-2">
        {notifications.map((notification) => (
          <Notification
            key={notification.id}
            message={notification.message}
            type={notification.type}
          />
        ))}
      </div>
    </div>
  );
};

export default TaskManager;
