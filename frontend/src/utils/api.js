/**
 * API Client for PLAGIATTRACKER
 */
import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'https://plagiattracker-backend.onrender.com'

const api = axios.create({
  baseURL: `${API_URL}/api/v1`,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Auth API
export const authAPI = {
  register: (email, password, fullName) =>
    api.post('/auth/register', { email, password, full_name: fullName }),

  login: (email, password) =>
    api.post('/auth/login', { email, password }),

  activateCode: (email, code) =>
    api.post('/auth/activate', { code }, { params: { email } }),

  getMe: (email) =>
    api.get('/auth/me', { params: { email } }),

  getPlans: () =>
    api.get('/auth/plans'),
}

// Upload API
export const uploadAPI = {
  uploadDocument: (email, file) => {
    const formData = new FormData()
    formData.append('file', file)

    return api.post('/upload', formData, {
      params: { email },
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },

  getDocument: (email, documentId) =>
    api.get(`/document/${documentId}`, { params: { email } }),
}

// Report API
export const reportAPI = {
  analyze: (email, documentId) =>
    api.post(`/analyze/${documentId}`, null, { params: { email } }),

  getReport: (email, documentId) =>
    api.get(`/report/${documentId}`, { params: { email } }),
}

export default api
