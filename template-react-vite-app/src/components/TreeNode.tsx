import { useState, useEffect } from 'react';
import { TreeNodeData } from '../services/domainService';
import { calculateXPProgress } from '../utils/xpCalculator';

interface TreeNodeProps {
  node: TreeNodeData;
  depth: number;
  isLast?: boolean;
  maxDepth?: number;
}

const TreeNode = ({ node, depth, isLast = false, maxDepth = 2 }: TreeNodeProps) => {
  const [isExpanded, setIsExpanded] = useState(depth < maxDepth); // Auto expand based on maxDepth

  // Update expansion state when maxDepth changes
  useEffect(() => {
    setIsExpanded(depth < maxDepth);
  }, [maxDepth, depth]);

  const hasChildren = node.hasChildren && Object.keys(node.children).length > 0;
  
  // Create tree line indicators
  const getTreeLines = () => {
    const lines = [];
    for (let i = 0; i < depth; i++) {
      lines.push(
        <span key={i} className="w-4 h-4 border-l border-gray-300 ml-2"></span>
      );
    }
    return lines;
  };

  const toggleExpanded = () => {
    if (hasChildren) {
      setIsExpanded(!isExpanded);
    }
  };

  // Color intensity based on level
  const getLevelColor = (level: number) => {
    if (level === 0) return 'bg-gray-100 text-gray-600';
    if (level <= 2) return 'bg-blue-100 text-blue-700';
    if (level <= 4) return 'bg-green-100 text-green-700';
    return 'bg-purple-100 text-purple-700';
  };

  // Remove unused function
  // const getProgressWidth = () => {
  //   if (node.hasChildren) {
  //     // For parent nodes, show progress based on children
  //     const maxPossibleXP = node.totalXpWithChildren * 1.2; // Assume 20% buffer
  //     return Math.min((node.totalXpWithChildren / maxPossibleXP) * 100, 100);
  //   } else {
  //     // For leaf nodes, show individual progress
  //     const baseXP = 1000; // Base XP for next level
  //     return Math.min((node.xp / baseXP) * 100, 100);
  //   }
  // };

  // Tính tiến độ XP tới level tiếp theo
  // - Với folder có children: dùng tổng XP (bao gồm children) để phản ánh đúng thanh tiến độ
  // - Với leaf: dùng XP của chính node
  const xpForProgress = node.hasChildren ? node.totalXpWithChildren : node.xp;
  const progress = calculateXPProgress(xpForProgress, node.streakDays || 0);

  return (
    <div className="select-none">
      {/* Current Node */}
      <div className="flex items-center">
        {/* Tree Lines */}
        {depth > 0 && (
          <div className="flex">
            {getTreeLines()}
            <span className={`w-4 h-4 ${isLast ? 'border-l border-b' : 'border-l'} border-gray-300`}>
              <span className="block w-4 h-2 border-b border-gray-300"></span>
            </span>
          </div>
        )}
        
        {/* Expand/Collapse Button */}
        <button
          onClick={toggleExpanded}
          className={`w-6 h-6 flex items-center justify-center text-xs ${
            hasChildren 
              ? 'text-blue-600 hover:text-blue-800 cursor-pointer' 
              : 'text-gray-400 cursor-default'
          }`}
        >
          {hasChildren ? (isExpanded ? '📂' : '📁') : '📄'}
        </button>

        {/* Node Content - Compact */}
        <div className="flex-1 ml-2">
          <div className="bg-gray-50 border border-gray-200 rounded p-2 hover:bg-gray-100 transition-colors">
            {/* Header - Compact */}
            <div className="flex justify-between items-center">
              <div className="flex items-center gap-2 flex-1 min-w-0">
                <span className="font-medium text-gray-800 truncate" title={node.name}>
                  {node.name}
                </span>
                {hasChildren && (
                  <span className="text-xs text-gray-500 shrink-0">
                    ({node.childrenCount})
                  </span>
                )}
              </div>
               <div className="flex items-center gap-1 shrink-0">
                 <span className="text-xs text-gray-400 bg-gray-200 px-1 rounded">
                   D{depth}
                 </span>
                 <span className={`px-1.5 py-0.5 rounded text-xs font-medium ${getLevelColor(progress.level)}`}>
                   L{progress.level}
                 </span>
               </div>
            </div>

            {/* Stats - Inline */}
            <div className="mt-1 flex justify-between text-xs text-gray-600">
              <span className="flex items-center gap-1">
                {node.hasChildren ? (
                  <>
                    <span className="font-medium">{node.totalXpWithChildren.toLocaleString()} XP</span>
                    <span className="text-gray-400">·</span>
                    <span title="XP của các file nằm trực tiếp trong folder này (không tính con)" className="text-gray-500">leaf {node.xp.toLocaleString()}</span>
                  </>
                ) : (
                  <span className="font-medium">{node.xp.toLocaleString()} XP</span>
                )}
              </span>
              <span>
                {node.hasChildren ? 
                  `${node.totalArticlesWithChildren} files` : 
                  `${node.taskCount} files`
                }
              </span>
              <div className="flex items-center gap-1">
                <span title={`Current streak: ${node.streakDays} days`}>
                  🔥 {node.streakDays}d
                </span>
                <span className="text-gray-400">|</span>
                <span title={`Max historical streak: ${node.maxStreakDays} days`}>
                  🏆 {node.maxStreakDays}d
                </span>
                <span className="text-gray-400">|</span>
                <span title={`Total days since first activity: ${node.totalDays} days`}>
                  📅 {node.totalDays}d
                </span>
              </div>
            </div>

            {/* XP Progress tới level tiếp theo */}
            <div className="mt-1">
              <div className="flex justify-between text-[10px] text-gray-500 mb-1">
                <span>XP: {xpForProgress.toLocaleString()}</span>
                <span>
                  {progress.currentXP}/{progress.requiredXP}
                </span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-1.5">
                <div
                  className="h-1.5 rounded-full transition-all duration-300"
                  style={{ width: `${progress.percentage}%`, backgroundColor: node.color }}
                />
              </div>
              {/* ETA tới level tiếp theo (ước lượng theo XP/ngày lịch sử) */}
              <div className="mt-1 flex justify-end text-[10px] text-gray-500">
                {(() => {
                  const xpPerDay = Math.max(1, Math.floor(node.xp / Math.max(1, node.totalDays)));
                  const remaining = Math.max(0, progress.requiredXP - progress.currentXP);
                  const etaDays = Math.ceil(remaining / xpPerDay);
                  return <span>~{etaDays}d to next level</span>;
                })()}
              </div>
            </div>
            
          </div>
        </div>
      </div>

      {/* Children */}
      {hasChildren && isExpanded && (
        <div className="mt-1">
          {depth < maxDepth ? (
            // Show children normally
            Object.entries(node.children).map(([childName, childNode], index) => {
              const isLastChild = index === Object.entries(node.children).length - 1;
              return (
                <TreeNode
                  key={childName}
                  node={childNode}
                  depth={depth + 1}
                  isLast={isLastChild}
                  maxDepth={maxDepth}
                />
              );
            })
          ) : (
            // Show truncated indicator
            <div className="flex items-center ml-6">
              <span className="text-xs text-gray-500 italic bg-gray-100 px-2 py-1 rounded">
                ... {node.childrenCount} subfolders (max depth reached)
              </span>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default TreeNode;
