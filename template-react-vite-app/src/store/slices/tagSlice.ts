import { createSlice, PayloadAction, createAsyncThunk } from '@reduxjs/toolkit';
import { fetchDomains, refreshDomains, DomainData } from '../../services/domainService';

export interface Tag {
  xp: number;
  level: number;
  color: string;
  taskCount: number;
  streakDays: number;
  lastTaskDate: string;
}

interface TagState {
  tags: Record<string, Tag>;
  domains: Record<string, Tag>;
  loading: boolean;
  error: string | null;
  lastDomainUpdate: string | null;
}

const getTagColor = (tagName: string) => {
  const colorPalette: Record<string, string> = {
    'Công việc': '#4F46E5', // Indigo
    'Học tập': '#10B981', // Emerald
    'Sức khỏe': '#F59E0B', // Amber
    'Gia đình': '#EC4899', // Pink
    'Giải trí': '#3B82F6', // Blue
    'Tài chính': '#8B5CF6', // Violet
    'Mối quan hệ': '#EF4444', // Red
    'Phát triển bản thân': '#14B8A6', // Teal
    'default': '#6B7280', // Gray
  };
  return colorPalette[tagName] || colorPalette.default;
};

const initialState: TagState = {
  tags: JSON.parse(localStorage.getItem('tags') || '{}'),
  domains: {},
  loading: false,
  error: null,
  lastDomainUpdate: null,
};

// Async thunks
export const loadDomains = createAsyncThunk(
  'tags/loadDomains',
  async () => {
    const response = await fetchDomains();
    return response;
  }
);

export const refreshDomainsData = createAsyncThunk(
  'tags/refreshDomains',
  async () => {
    const response = await refreshDomains();
    return response;
  }
);

const tagSlice = createSlice({
  name: 'tags',
  initialState,
  reducers: {
    addTagXP: (
      state,
      action: PayloadAction<{ tagName: string; value: number; date: string }>,
    ) => {
      const { tagName, value, date } = action.payload;
      if (!state.tags[tagName]) {
        state.tags[tagName] = {
          xp: 0,
          level: 0,
          color: getTagColor(tagName),
          taskCount: 0,
          streakDays: 0,
          lastTaskDate: date,
        };
      }

      // Update streak
      const lastDate = new Date(state.tags[tagName].lastTaskDate);
      const currentDate = new Date(date);
      const dayDiff = Math.floor(
        (currentDate.getTime() - lastDate.getTime()) / (1000 * 60 * 60 * 24),
      );

      if (dayDiff === 1) {
        // Consecutive day
        state.tags[tagName].streakDays += 1;
      } else if (dayDiff > 1) {
        // Streak broken
        state.tags[tagName].streakDays = 1;
      }

      state.tags[tagName].lastTaskDate = date;

      const xpToAdd = Math.abs(value);
      state.tags[tagName].xp += xpToAdd;
      state.tags[tagName].taskCount = (state.tags[tagName].taskCount || 0) + 1;
      state.tags[tagName].level = calculateLevel(state.tags[tagName].xp);

      localStorage.setItem('tags', JSON.stringify(state.tags));
    },
    removeTagXP: (
      state,
      action: PayloadAction<{ tagName: string; value: number }>,
    ) => {
      const { tagName, value } = action.payload;
      if (state.tags[tagName]) {
        const xpToRemove = Math.abs(value);
        state.tags[tagName].xp = Math.max(
          0,
          state.tags[tagName].xp - xpToRemove,
        );
        state.tags[tagName].level = calculateLevel(state.tags[tagName].xp);
        state.tags[tagName].taskCount = Math.max(
          0,
          (state.tags[tagName].taskCount || 0) - 1,
        );
        localStorage.setItem('tags', JSON.stringify(state.tags));
      }
    },
    updateTag: (
      state,
      action: PayloadAction<{ name: string; changes: Partial<Tag> }>,
    ) => {
      const { name, changes } = action.payload;
      if (state.tags[name]) {
        state.tags[name] = { ...state.tags[name], ...changes };
      }
    },
    removeTag: (state, action: PayloadAction<string>) => {
      const tagName = action.payload;
      if (state.tags[tagName]) {
        delete state.tags[tagName];
        localStorage.setItem('tags', JSON.stringify(state.tags));
      }
    },
    clearError: (state) => {
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      // Load domains
      .addCase(loadDomains.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(loadDomains.fulfilled, (state, action) => {
        state.loading = false;
        state.domains = action.payload.domains;
        state.lastDomainUpdate = action.payload.last_scan;
        state.error = null;
      })
      .addCase(loadDomains.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to load domains';
      })
      // Refresh domains
      .addCase(refreshDomainsData.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(refreshDomainsData.fulfilled, (state, action) => {
        state.loading = false;
        state.domains = action.payload.domains;
        state.lastDomainUpdate = action.payload.last_scan;
        state.error = null;
      })
      .addCase(refreshDomainsData.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to refresh domains';
      });
  },
});

const calculateLevel = (xp: number): number => {
  let level = 0;
  let requiredXP = 1000; // Base XP required for level 1
  const LEVEL_XP_MULTIPLIER = 1.5;

  while (xp >= requiredXP) {
    level++;
    xp -= requiredXP;
    requiredXP = Math.floor(1000 * Math.pow(LEVEL_XP_MULTIPLIER, level));
  }

  return level;
};

export const { addTagXP, removeTagXP, updateTag, removeTag, clearError } = tagSlice.actions;

export default tagSlice.reducer;
