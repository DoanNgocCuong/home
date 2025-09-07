import { Provider } from 'react-redux';
import { store } from './store';
import TaskManager from './pages/TaskManager';
import AppHeader from './components/AppHeader';
import { Analytics } from '@vercel/analytics/react';
import { injectSpeedInsights } from '@vercel/speed-insights';
import './App.css';

function App() {
  // Initialize Speed Insights
  injectSpeedInsights();

  return (
    <Provider store={store}>
      <div className="min-h-screen bg-gray-100 p-4">
        <AppHeader />
        <TaskManager />
        <Analytics />
      </div>
    </Provider>
  );
}

export default App;
