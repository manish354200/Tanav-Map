import axios from 'axios';

const API_BASE_URL =
  import.meta?.env?.VITE_API_URL ||
  'http://localhost:8000/api/v1';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

apiClient.interceptors.request.use((config) => {
  const savedSession = localStorage.getItem('mental-health-session');
  if (savedSession) {
    config.headers.Authorization = `Bearer ${JSON.parse(savedSession).access_token}`;
  }
  return config;
});

export const authAPI = {
  signup: (data) => apiClient.post('/auth/signup', data),
  login: (email, password) => {
    const form = new URLSearchParams({ username: email, password });
    return apiClient.post('/auth/login', form, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    });
  },
};

export const victimAPI = {
  getAll: (page = 1, pageSize = 10) => 
    apiClient.get(`/victims?page=${page}&page_size=${pageSize}`),
  get: (id) => apiClient.get(`/victims/${id}`),
  create: (data) => apiClient.post('/victims', data),
  update: (id, data) => apiClient.put(`/victims/${id}`, data),
};

export const interactionAPI = {
  logText: (victimId, message, channel = 'chatbot') =>
    apiClient.post('/interactions/text', { victim_id: victimId, message, channel }),
  getHistory: (victimId, limit = 10) =>
    apiClient.get(`/interactions/${victimId}/history?limit=${limit}`),
};

export const analysisAPI = {
  analyze: (victimId) => apiClient.post(`/analysis/${victimId}/analyze`),
  getDistressScore: (victimId) => apiClient.get(`/analysis/${victimId}/distress-score`),
  getDistressTrend: (victimId, days = 30) => 
    apiClient.get(`/analysis/${victimId}/distress-trend?days=${days}`),
};

export const dashboardAPI = {
  getDistrict: (district) => apiClient.get(`/dashboard/district?district=${district}`),
  getState: (state) => apiClient.get(`/dashboard/state?state=${state}`),
  getNational: () => apiClient.get('/dashboard/national'),
};

export const alertAPI = {
  getAll: (status, level, limit = 20) =>
    apiClient.get(`/alerts?status=${status}&level=${level}&limit=${limit}`),
  get: (id) => apiClient.get(`/alerts/${id}`),
  acknowledge: (id) => apiClient.post(`/alerts/${id}/acknowledge`),
};

export const interventionAPI = {
  getRecommendations: (victimId) => 
    apiClient.get(`/interventions/${victimId}`),
  create: (victimId, type, notes) =>
    apiClient.post(`/interventions/${victimId}/recommend`, { 
      intervention_type: type, 
      notes 
    }),
  approve: (id, approvedBy) =>
    apiClient.post(`/interventions/${id}/approve`, { approved_by: approvedBy }),
  execute: (id) => apiClient.post(`/interventions/${id}/execute`),
};

export const assistantAPI = {
  respond: (message, victimId = 1, history = [], language = 'english') =>
    apiClient.post('/assistant/response', {
      message,
      victim_id: victimId,
      history,
      language,
    }),
};

export default apiClient;
