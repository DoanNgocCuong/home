import { configureStore } from '@reduxjs/toolkit';
import taskReducer from './slices/taskSlice';
import tagReducer from './slices/tagSlice';

export const store = configureStore({
  reducer: {
    tasks: taskReducer,
    tags: tagReducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
