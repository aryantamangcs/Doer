import { endpoints } from "./endpoints";

import { fetcher, poster } from "@/lib/api/http";

import {
  setAccessToken,
  setRefreshToken,
  getRefreshToken,
} from "@/auth/services/token";

export const signUp = async (userData: any) => {
  try {
    const response = await poster([endpoints.auth.signUp, userData]);

    setAccessToken(response.data.access_token);
    setRefreshToken(response.data.refresh_token);

    return response.data;
  } catch (error) {
    throw error;
  }
};

export const signIn = async (userData: any) => {
  try {
    const response = await poster([endpoints.auth.signIn, userData]);

    const responseData = response.data;

    setAccessToken(responseData.access_token);
    setRefreshToken(responseData.refresh_token);

    return responseData;
  } catch (error) {
    throw error;
  }
};

export const checkUserAvailability = async (query: string) => {
  try {
    const url = `${endpoints.auth.checkUserAvailability}${query}`;

    const response = await fetcher(url);

    return response;
  } catch (error) {
    throw error;
  }
};

export const refreshAccessToken = async () => {
  try {
    const refreshToken = getRefreshToken();

    if (!refreshToken) throw new Error("No refresh token found");

    const response = await poster([
      endpoints.auth.refreshToken,
      {
        refresh_token: refreshToken,
      },
    ]);

    const responseData = response.data;

    setAccessToken(responseData.access_token);
    setRefreshToken(responseData.refresh_token);

    return responseData.access_token;
  } catch (error) {
    console.error("Failed to refresh token:", error);
    throw error;
  }
};
