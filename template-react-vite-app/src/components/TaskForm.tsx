import { useState, FormEvent } from 'react';
import { useSelector } from 'react-redux';
import { RootState } from '../store';
import { createSelector } from '@reduxjs/toolkit';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPlus, faTimes } from '@fortawesome/free-solid-svg-icons';
import { calculateStreakMultiplier } from '../utils/xpCalculator';

interface TaskFormProps {
  onSubmit: (data: {
    name: string;
    tags: string[];
    value: number;
    date: string;
  }) => void;
}

const selectTags = createSelector(
  (state: RootState) => state.tags,
  (tagsState) => tagsState.tags
);

const TaskForm = ({ onSubmit }: TaskFormProps) => {
  const tags = useSelector(selectTags);
  const [taskName, setTaskName] = useState('');
  const [taskValue, setTaskValue] = useState('');
  const [taskDate, setTaskDate] = useState(
    new Date().toISOString().split('T')[0],
  );
  const [selectedTags, setSelectedTags] = useState<string[]>([]);
  const [tagInput, setTagInput] = useState('');

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();

    if (!taskName || selectedTags.length === 0 || !taskValue || !taskDate) {
      return;
    }

    const value = parseInt(taskValue);
    if (value < -1000 || value > 1000) {
      alert('Giá trị task phải nằm trong khoảng -1000 đến 1000');
      return;
    }

    onSubmit({
      name: taskName,
      tags: selectedTags,
      value: value,
      date: taskDate,
    });

    // Reset form
    setTaskName('');
    setTaskValue('');
    setTaskDate(new Date().toISOString().split('T')[0]);
    setSelectedTags([]);
    setTagInput('');
  };

  const handleAddTag = () => {
    const tagName = tagInput.trim();
    if (tagName && !selectedTags.includes(tagName)) {
      setSelectedTags([...selectedTags, tagName]);
      setTagInput('');
    }
  };

  const handleRemoveTag = (tagToRemove: string) => {
    setSelectedTags(selectedTags.filter((tag) => tag !== tagToRemove));
  };

  const handleTagKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      handleAddTag();
    }
  };

  const sortedTags = Object.keys(tags).sort((a, b) => {
    const countDiff = (tags[b].taskCount || 0) - (tags[a].taskCount || 0);
    if (countDiff !== 0) return countDiff;

    const streakDiff = (tags[b].streakDays || 0) - (tags[a].streakDays || 0);
    if (streakDiff !== 0) return streakDiff;

    return tags[b].xp - tags[a].xp;
  });

  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <h2 className="text-xl font-semibold text-gray-800 mb-4">
        Thêm Task Mới
      </h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label
            htmlFor="taskName"
            className="block text-sm font-medium text-gray-700"
          >
            Tên Task
          </label>
          <input
            type="text"
            id="taskName"
            value={taskName}
            onChange={(e) => setTaskName(e.target.value)}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm p-2 border"
            required
          />
        </div>

        <div>
          <label
            htmlFor="taskTag"
            className="block text-sm font-medium text-gray-700"
          >
            Tags
          </label>
          <div className="flex flex-wrap gap-2 mb-2">
            {selectedTags.map((tag) => (
              <span
                key={tag}
                className="tag-pill inline-flex items-center"
                style={{
                  backgroundColor: tags[tag]
                    ? `${tags[tag].color}33`
                    : '#CBD5E033',
                  color: tags[tag] ? tags[tag].color : '#718096',
                }}
              >
                {tag}
                <button
                  type="button"
                  className="ml-1 text-xs hover:text-red-500"
                  onClick={() => handleRemoveTag(tag)}
                >
                  <FontAwesomeIcon icon={faTimes} />
                </button>
              </span>
            ))}
          </div>
          <div className="flex">
            <input
              type="text"
              id="taskTag"
              value={tagInput}
              onChange={(e) => setTagInput(e.target.value)}
              onKeyPress={handleTagKeyPress}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm p-2 border"
              placeholder="Nhập tag mới hoặc chọn từ danh sách"
              list="tagOptions"
            />
            <button
              type="button"
              onClick={handleAddTag}
              className="ml-2 bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded transition duration-300"
            >
              <FontAwesomeIcon icon={faPlus} />
            </button>
          </div>
          <datalist id="tagOptions">
            {Object.keys(tags).map((tag) => (
              <option key={tag} value={tag} />
            ))}
          </datalist>
          <div className="mt-2 flex flex-wrap gap-2">
            {sortedTags.slice(0, 5).map((tag) => {
              const streakMultiplier = calculateStreakMultiplier(
                tags[tag].streakDays || 0,
              );
              return (
                <button
                  key={tag}
                  type="button"
                  onClick={() => {
                    if (!selectedTags.includes(tag)) {
                      setSelectedTags([...selectedTags, tag]);
                    }
                  }}
                  className="tag-pill text-xs hover:opacity-80 transition-opacity"
                  style={{
                    backgroundColor: `${tags[tag].color}33`,
                    color: tags[tag].color,
                  }}
                >
                  {tag}
                  <span className="ml-1 text-xs opacity-70">
                    ({tags[tag].taskCount || 0}, x{streakMultiplier})
                  </span>
                </button>
              );
            })}
          </div>
        </div>

        <div>
          <label
            htmlFor="taskValue"
            className="block text-sm font-medium text-gray-700"
          >
            Giá Trị (KINH NGHIỆM)
          </label>
          <input
            type="number"
            id="taskValue"
            value={taskValue}
            onChange={(e) => setTaskValue(e.target.value)}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm p-2 border"
            required
            min="-1000"
            max="1000"
          />
          <p className="text-sm text-gray-500 mt-1">
            Nhập số từ 1 đến 1000 cho kinh nghiệm tích lũy, số âm từ -1 đến
            -1000 cho kinh nghiệm tiêu hao
          </p>
        </div>

        <div>
          <label
            htmlFor="taskDate"
            className="block text-sm font-medium text-gray-700"
          >
            Ngày
          </label>
          <input
            type="date"
            id="taskDate"
            value={taskDate}
            onChange={(e) => setTaskDate(e.target.value)}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm p-2 border"
            required
          />
        </div>

        <button
          type="submit"
          className="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded transition duration-300"
        >
          Thêm Task
        </button>
      </form>
    </div>
  );
};

export default TaskForm;
