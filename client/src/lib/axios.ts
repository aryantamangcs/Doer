import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse } from "axios";

import { CONFIG } from "@/global-config";

// ----------------------------------------------------------------------

const axiosInstance: AxiosInstance = axios.create({
  baseURL: CONFIG.serverUrl,
});

axiosInstance.interceptors.response.use(
  (response: AxiosResponse) => response,
  (error) =>
    Promise.reject(
      (error.response && error.response.data) || "Something went wrong!"
    )
);

// ----------------------------------------------------------------------

export default axiosInstance;

// ----------------------------------------------------------------------

type FetcherArgs = [string, AxiosRequestConfig?] | string;

export const fetcher = async <T = any>(args: FetcherArgs): Promise<T> => {
  try {
    const [url, config] = Array.isArray(args) ? args : [args, undefined];

    const res: AxiosResponse<T> = await axiosInstance.get(url, { ...config });

    return res.data;
  } catch (error: any) {
    console.error("Failed to fetch:", error);
    throw error;
  }
};

type PosterArgs = [string, any, AxiosRequestConfig?] | [string, any];

export const poster = async <T = any>(args: PosterArgs): Promise<T> => {
  try {
    const [url, data, config] = Array.isArray(args)
      ? args.length === 2
        ? [args[0], args[1], undefined]
        : args
      : [args, undefined, undefined];

    const res: AxiosResponse<T> = await axiosInstance.post(url, data, {
      ...config,
    });

    return res.data;
  } catch (error: any) {
    console.error("Failed to post:", error);
    throw error;
  }
};
