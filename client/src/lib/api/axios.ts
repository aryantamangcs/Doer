import axios, { AxiosInstance, AxiosResponse, isAxiosError } from "axios";

import { paths } from "@/routes/paths";

import {
  getAccessToken,
  deleteAccessToken,
  //
  deleteRefreshToken,
} from "@/auth/services/token";

import { refreshAccessToken } from "@/api/auth";

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

    console.log(error);

    if (error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const newAccessToken = await refreshAccessToken();

        originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;

        return axiosInstance(originalRequest);
      } catch (refreshError) {
        deleteAccessToken();

        deleteRefreshToken();

        window.location.href = paths.auth.signIn;

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
