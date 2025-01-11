// src/lib/axios-client.ts
import axios from 'axios'
import {
  getAccessToken,
  getRefreshToken,
  setTokens,
  clearTokens,
} from './utils'

const BASE_URL = import.meta.env.VITE_API_URL

const axiosClient = axios.create({
  baseURL: BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true,
})

// Request interceptor for adding auth token
axiosClient.interceptors.request.use(
  (config) => {
    const token = getAccessToken()
    // console.log('Current token:', token)
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
      config.headers['Access-Control-Allow-Credentials'] = 'true'
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor for handling token refresh
axiosClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config

    // If error is 401 and we haven't tried to refresh token yet
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      try {
        const refreshToken = getRefreshToken()
        const response = await axios.post(
          `${BASE_URL}/auth/refresh`,
          {
            refresh_token: refreshToken,
          },
          {
            withCredentials: true,
          }
        )

        const { access_token, refresh_token } = response.data
        setTokens(access_token, refresh_token)

        // Retry original request with new token
        originalRequest.headers.Authorization = `Bearer ${access_token}`
        return axiosClient(originalRequest)
      } catch (error) {
        clearTokens()
        window.location.href = '/login'
        return Promise.reject(error)
      }
    }

    return Promise.reject(error)
  }
)

export default axiosClient
