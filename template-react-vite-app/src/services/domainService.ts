/**
 * Domain Service - API calls to backend
 */

const API_BASE_URL = 'http://localhost:8000';

export interface DomainData {
  xp: number;
  level: number;
  color: string;
  taskCount: number;
  streakDays: number;
  totalDays: number;
  lastTaskDate: string;
}

export interface DomainsResponse {
  success: boolean;
  domains: Record<string, DomainData>;
  count: number;
  last_scan: string;
}

export interface StatsResponse {
  success: boolean;
  stats: {
    total_domains: number;
    total_articles: number;
    total_xp: number;
    total_levels: number;
    average_level: number;
    highest_level_domain: [string, DomainData] | null;
    most_articles_domain: [string, DomainData] | null;
  };
  last_scan: string;
}

/**
 * Fetch all domains from backend
 */
export const fetchDomains = async (): Promise<DomainsResponse> => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/domains`);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching domains:', error);
    throw error;
  }
};

/**
 * Refresh domains data from backend
 */
export const refreshDomains = async (): Promise<DomainsResponse> => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/domains/refresh`, {
      method: 'POST',
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error refreshing domains:', error);
    throw error;
  }
};

/**
 * Fetch domain statistics
 */
export const fetchDomainStats = async (): Promise<StatsResponse> => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/domains/stats`);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching domain stats:', error);
    throw error;
  }
};

/**
 * Check if backend is available
 */
export const checkBackendHealth = async (): Promise<boolean> => {
  try {
    const response = await fetch(`${API_BASE_URL}/`);
    return response.ok;
  } catch (error) {
    console.error('Backend not available:', error);
    return false;
  }
};
