import { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { RootState } from '../store';
import { createSelector } from '@reduxjs/toolkit';
import { addTask, deleteTask, setCurrentDate } from '../store/slices/taskSlice';
import { addTagXP, removeTagXP } from '../store/slices/tagSlice';
import TaskForm from '../components/TaskForm';
import TaskList from '../components/TaskList';
import TagLevels from '../components/TagLevels';
import Charts from '../components/Charts';
import ExperienceOverview from '../components/ExperienceOverview';
import Notification from '../components/Notification';

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

  return (
    <div className="space-y-8">
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-1">
          <TaskForm onSubmit={handleAddTask} />
        </div>
        <div className="lg:col-span-2">
          <TagLevels tags={tags} />
        </div>
      </div>

      <TaskList
        tasks={tasks}
        currentDate={currentDate}
        onDeleteTask={handleDeleteTask}
        onDateChange={handleDateChange}
      />

      <Charts tasks={tasks} tags={tags} />

      <ExperienceOverview tasks={tasks} tags={tags} />

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
