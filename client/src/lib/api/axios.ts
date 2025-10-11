import axios, { AxiosInstance, AxiosResponse } from "axios";

import {
  getAccessToken,
  setAccessToken,
  deleteAccessToken,
  //
  getRefreshToken,
  deleteRefreshToken,
} from "@/auth/services/token";

import { CONFIG } from "@/global-config";

const axiosInstance: AxiosInstance = axios.create({
  baseURL: CONFIG.serverUrl,
});

axiosInstance.interceptors.request.use(
  (config) => {
    const token = getAccessToken();

    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

axiosInstance.interceptors.response.use(
  (response: AxiosResponse) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = getRefreshToken();
        if (!refreshToken) throw new Error("No refresh token");

        const res = await axios.post(`${CONFIG.serverUrl}/auth/refresh`, {
          refresh_token: refreshToken,
        });

        const newAccessToken = res.data?.access_token;

        setAccessToken(newAccessToken);

        originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
        return axiosInstance(originalRequest);
      } catch (refreshError) {
        deleteAccessToken();
        deleteRefreshToken();

        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(
      error.response?.data || error.message || "Something went wrong!"
    );
  }
);

// ----------------------------------------------------------------------

export default axiosInstance;
