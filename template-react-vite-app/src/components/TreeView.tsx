import { useState, useEffect } from 'react';
import { TreeResponse, fetchTreeData } from '../services/domainService';
import TreeNode from './TreeNode';

interface TreeViewProps {
  className?: string;
}

const TreeView = ({ className = '' }: TreeViewProps) => {
  const [treeData, setTreeData] = useState<TreeResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [maxDepth, setMaxDepth] = useState<number>(2); // Default to 2 levels

  const loadTreeData = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await fetchTreeData();
      setTreeData(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Lỗi không xác định');
      console.error('Error loading tree data:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadTreeData();
  }, []);

  const handleRefresh = () => {
    loadTreeData();
  };

  const getTreeStats = () => {
    if (!treeData) return null;

    let totalNodes = 0;
    let totalXP = 0;
    let totalFiles = 0;
    let maxLevel = 0;

    const countNodes = (nodes: Record<string, any>) => {
      Object.values(nodes).forEach((node: any) => {
        totalNodes++;
        totalXP += node.totalXpWithChildren || node.xp;
        totalFiles += node.totalArticlesWithChildren || node.taskCount;
        maxLevel = Math.max(maxLevel, node.maxLevelInTree || node.level);
        
        if (node.children) {
          countNodes(node.children);
        }
      });
    };

    countNodes(treeData.tree);

    return {
      totalNodes,
      totalXP,
      totalFiles,
      maxLevel,
      rootFolders: Object.keys(treeData.tree).length,
    };
  };

  const stats = getTreeStats();

  if (loading) {
    return (
      <div className={`bg-white p-6 rounded-lg shadow-md ${className}`}>
        <div className="flex items-center justify-center py-8">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
          <span className="ml-3 text-gray-600">Đang tải cấu trúc thư mục...</span>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className={`bg-white p-6 rounded-lg shadow-md ${className}`}>
        <div className="text-center py-8">
          <div className="text-red-500 mb-4">
            <svg className="mx-auto h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.732-.833-2.5 0L4.314 16.5c-.77.833.192 2.5 1.732 2.5z" />
            </svg>
          </div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">Lỗi tải dữ liệu</h3>
          <p className="text-gray-600 mb-4">{error}</p>
          <button
            onClick={handleRefresh}
            className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
          >
            Thử lại
          </button>
        </div>
      </div>
    );
  }

  if (!treeData || Object.keys(treeData.tree).length === 0) {
    return (
      <div className={`bg-white p-6 rounded-lg shadow-md ${className}`}>
        <div className="text-center py-8 text-gray-500">
          <div className="text-6xl mb-4">📁</div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">Không có dữ liệu</h3>
          <p className="text-gray-600 mb-4">Chưa tìm thấy thư mục nào.</p>
          <button
            onClick={handleRefresh}
            className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
          >
            Tải lại
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className={`bg-white rounded-lg ${className.includes('shadow-none') ? '' : 'shadow-md'} ${className.includes('border-0') ? '' : 'border border-gray-200'}`}>
      {/* Compact Header */}
      <div className="p-4 border-b border-gray-200">
        <div className="flex justify-between items-center">
          <div>
            <h3 className="text-lg font-semibold text-gray-800">
              📁 Domain Structure
            </h3>
            <p className="text-xs text-gray-500 mt-1">
              {stats && `${stats.totalNodes} folders • ${stats.totalFiles.toLocaleString()} files • ${stats.totalXP.toLocaleString()} XP`}
            </p>
          </div>
          
          <div className="flex items-center gap-2">
            {/* Depth Control */}
            <div className="flex items-center gap-1">
              <span className="text-xs text-gray-500">Depth:</span>
              {[1, 2, 3].map((depth) => (
                <button
                  key={depth}
                  onClick={() => setMaxDepth(depth)}
                  className={`px-2 py-1 text-xs rounded transition-colors ${
                    maxDepth === depth
                      ? 'bg-blue-500 text-white'
                      : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                  }`}
                >
                  {depth}
                </button>
              ))}
            </div>
            
            {/* Refresh Button */}
            <button
              onClick={handleRefresh}
              disabled={loading}
              className="px-3 py-1 bg-blue-500 text-white rounded text-xs hover:bg-blue-600 disabled:opacity-50 transition-colors flex items-center gap-1"
            >
              <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
              {loading ? 'Loading...' : 'Refresh'}
            </button>
          </div>
        </div>

        {/* Compact Stats */}
        {stats && (
          <div className="mt-3 grid grid-cols-3 gap-2">
            <div className="bg-blue-50 p-2 rounded text-center">
              <div className="text-sm font-bold text-blue-600">{stats.rootFolders}</div>
              <div className="text-xs text-blue-700">Roots</div>
            </div>
            <div className="bg-green-50 p-2 rounded text-center">
              <div className="text-sm font-bold text-green-600">{stats.totalNodes}</div>
              <div className="text-xs text-green-700">Folders</div>
            </div>
            <div className="bg-purple-50 p-2 rounded text-center">
              <div className="text-sm font-bold text-purple-600">{stats.maxLevel}</div>
              <div className="text-xs text-purple-700">Max Level</div>
            </div>
          </div>
        )}
      </div>

      {/* Tree Content - Compact */}
      <div className="p-4">
        <div className="space-y-1">
          {Object.entries(treeData.tree).map(([rootName, rootNode], index) => {
            const isLast = index === Object.entries(treeData.tree).length - 1;
            return (
              <TreeNode
                key={rootName}
                node={rootNode}
                depth={0}
                isLast={isLast}
                maxDepth={maxDepth}
              />
            );
          })}
        </div>
      </div>
    </div>
  );
};

export default TreeView;
