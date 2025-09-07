import { Tag } from '../store/slices/tagSlice';
import {
  calculateXPProgress,
  calculateStreakMultiplier,
  calculateMilestoneBonus,
} from '../utils/xpCalculator';
import { useDispatch } from 'react-redux';
import { updateTag, removeTag } from '../store/slices/tagSlice';
import { useState } from 'react';

interface TagLevelsProps {
  tags: Record<string, Tag>;
}

const TagLevels = ({ tags }: TagLevelsProps) => {
  const dispatch = useDispatch();
  const [editingTag, setEditingTag] = useState<string | null>(null);
  const [tagToDelete, setTagToDelete] = useState<string | null>(null);

  const handleColorChange = (tagName: string, color: string) => {
    dispatch(
      updateTag({
        name: tagName,
        changes: { color },
      }),
    );
    setEditingTag(null);
  };

  const handleDeleteTag = (tagName: string) => {
    dispatch(removeTag(tagName));
    setTagToDelete(null);
  };

  const sortedTags = Object.keys(tags).sort((a, b) => {
    if (tags[b].level !== tags[a].level) {
      return tags[b].level - tags[a].level;
    }
    return tags[b].xp - tags[a].xp;
  });

  // Log tag calculations
  console.log('=== Tag Level Calculations ===');
  sortedTags.forEach((tagName) => {
    const tag = tags[tagName];
    const streakMultiplier = calculateStreakMultiplier(tag.streakDays || 0);
    const progress = calculateXPProgress(tag.xp, tag.streakDays || 0);
    const milestoneBonus = calculateMilestoneBonus((tag.streakDays || 0) / 365);

    console.log(`\nTag: ${tagName}`);
    console.log('Base XP:', tag.xp);
    console.log('Streak Days:', tag.streakDays || 0);
    console.log('Streak Multiplier:', streakMultiplier);
    console.log(
      'Total XP (after multiplier):',
      Math.floor(tag.xp * streakMultiplier),
    );
    console.log('Current Level:', progress.level);
    console.log('Current XP in Level:', progress.currentXP);
    console.log('Required XP for Next Level:', progress.requiredXP);
    console.log('Progress Percentage:', progress.percentage.toFixed(2) + '%');
    console.log('Milestone Bonus:', milestoneBonus);
  });

  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <h2 className="text-xl font-semibold text-gray-800 mb-4">
        Level của Các Tag
      </h2>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {sortedTags.length === 0 ? (
          <div className="col-span-full text-center py-4 text-gray-500">
            Chưa có tag nào. Hãy thêm task mới để tạo tag!
          </div>
        ) : (
          sortedTags.map((tagName) => {
            const tag = tags[tagName];
            const streakMultiplier = calculateStreakMultiplier(
              tag.streakDays || 0,
            );
            const progress = calculateXPProgress(tag.xp, tag.streakDays || 0);
            const milestoneBonus = calculateMilestoneBonus(
              (tag.streakDays || 0) / 365,
            );

            return (
              <div key={tagName} className="bg-gray-50 p-4 rounded-lg border">
                <div className="flex justify-between items-center">
                  <div className="flex items-center gap-2">
                    <span
                      className="tag-pill cursor-pointer hover:opacity-80 transition-opacity"
                      style={{
                        backgroundColor: `${tag.color}33`,
                        color: tag.color,
                      }}
                      onClick={() =>
                        setEditingTag(editingTag === tagName ? null : tagName)
                      }
                    >
                      {tagName}
                    </span>
                    <button
                      onClick={() => setTagToDelete(tagName)}
                      className="text-gray-400 hover:text-red-500 transition-colors"
                    >
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        className="h-5 w-5"
                        viewBox="0 0 20 20"
                        fill="currentColor"
                      >
                        <path
                          fillRule="evenodd"
                          d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z"
                          clipRule="evenodd"
                        />
                      </svg>
                    </button>
                    {editingTag === tagName && (
                      <div className="absolute z-10 mt-8 bg-white p-2 rounded shadow-lg">
                        <div className="grid grid-cols-4 gap-1">
                          {[
                            '#4F46E5',
                            '#059669',
                            '#DC2626',
                            '#6B7280',
                            '#F59E0B',
                            '#10B981',
                            '#3B82F6',
                            '#8B5CF6',
                          ].map((color) => (
                            <button
                              key={color}
                              className="w-6 h-6 rounded-full border-2 border-gray-200 hover:border-gray-400 transition-colors"
                              style={{ backgroundColor: color }}
                              onClick={() => handleColorChange(tagName, color)}
                            />
                          ))}
                        </div>
                        <input
                          type="color"
                          value={tag.color}
                          onChange={(e) =>
                            handleColorChange(tagName, e.target.value)
                          }
                          className="mt-2 w-full h-8 rounded border border-gray-300"
                        />
                      </div>
                    )}
                  </div>
                  <span className="text-indigo-700 font-bold">
                    Level {progress.level}
                  </span>
                </div>
                <div className="mt-2">
                  <div className="flex justify-between text-xs text-gray-500 mb-1">
                    <span>XP: {tag.xp}</span>
                    <span>
                      {progress.currentXP}/{progress.requiredXP}
                    </span>
                  </div>
                  <div className="progress-bar">
                    <div
                      className="progress-fill"
                      style={{
                        width: `${progress.percentage}%`,
                        backgroundColor: tag.color,
                      }}
                    />
                  </div>
                </div>
                <div className="mt-2 text-xs text-gray-500 space-y-1">
                  <div>
                    <span>{tag.taskCount || 0} task đã hoàn thành</span>
                  </div>
                  <div>
                    <span>
                      Streak: {tag.streakDays || 0} ngày (x{streakMultiplier})
                    </span>
                  </div>
                  {milestoneBonus > 0 && (
                    <div className="text-green-600">
                      <span>Bonus mốc: +{milestoneBonus} XP</span>
                    </div>
                  )}
                </div>
              </div>
            );
          })
        )}
      </div>

      {/* Delete Confirmation Dialog */}
      {tagToDelete && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white p-6 rounded-lg shadow-xl max-w-md w-full mx-4">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              Xác nhận xóa tag
            </h3>
            <p className="text-gray-600 mb-6">
              Bạn có chắc chắn muốn xóa tag "{tagToDelete}"? Hành động này không
              thể hoàn tác.
            </p>
            <div className="flex justify-end gap-4">
              <button
                onClick={() => setTagToDelete(null)}
                className="px-4 py-2 text-gray-600 hover:text-gray-800 transition-colors"
              >
                Hủy
              </button>
              <button
                onClick={() => handleDeleteTag(tagToDelete)}
                className="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600 transition-colors"
              >
                Xóa
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default TagLevels;
