import { getCookie, setCookie, deleteCookie } from "@/lib/cookies/cookie";

const ACCESS_TOKEN_KEY = "access_token";
const REFRESH_TOKEN_KEY = "refresh_token";

export const getAccessToken = () => getCookie(ACCESS_TOKEN_KEY);
export const setAccessToken = (token: string) =>
  setCookie(ACCESS_TOKEN_KEY, token, { secure: true });
export const deleteAccessToken = () => deleteCookie(ACCESS_TOKEN_KEY);

export const getRefreshToken = () => getCookie(REFRESH_TOKEN_KEY);
export const setRefreshToken = (token: string) =>
  setCookie(REFRESH_TOKEN_KEY, token, { secure: true });
export const deleteRefreshToken = () => deleteCookie(REFRESH_TOKEN_KEY);
