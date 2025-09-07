import { createSlice, PayloadAction } from '@reduxjs/toolkit';

export interface Task {
  id: number;
  name: string;
  tags: string[];
  value: number;
  date: string;
  timestamp: number;
}

interface TaskState {
  tasks: Task[];
  currentDate: string;
}

const initialState: TaskState = {
  tasks: JSON.parse(localStorage.getItem('tasks') || '[]'),
  currentDate: new Date().toISOString().split('T')[0],
};

const taskSlice = createSlice({
  name: 'tasks',
  initialState,
  reducers: {
    addTask: (state, action: PayloadAction<Omit<Task, 'id' | 'timestamp'>>) => {
      const newTask: Task = {
        ...action.payload,
        id: Date.now(),
        timestamp: Date.now(),
      };
      state.tasks.push(newTask);
      localStorage.setItem('tasks', JSON.stringify(state.tasks));
    },
    deleteTask: (state, action: PayloadAction<number>) => {
      state.tasks = state.tasks.filter((task) => task.id !== action.payload);
      localStorage.setItem('tasks', JSON.stringify(state.tasks));
    },
    setCurrentDate: (state, action: PayloadAction<string>) => {
      state.currentDate = action.payload;
    },
  },
});

export const { addTask, deleteTask, setCurrentDate } = taskSlice.actions;
export default taskSlice.reducer;
