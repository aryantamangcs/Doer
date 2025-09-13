import { endpoints } from "./endpoints";

import { poster } from "@/lib/axios";

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

    return response.data;
  } catch (error) {
    throw error;
  }
};
