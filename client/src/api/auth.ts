import { endpoints } from "./endpoints";

import { fetcher, poster } from "@/lib/api/http";

import { setAccessToken, setRefreshToken } from "@/auth/services/token";

export const signUp = async (userData: any) => {
  try {
    const response = await poster([endpoints.auth.signUp, userData]);

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
