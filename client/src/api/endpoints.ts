export const endpoints = {
  auth: {
    signIn: "api/auth/login",
    signUp: "api/auth/signup",
    checkUserAvailability: "/api/auth/check-user",
    refreshToken: "/api/auth/refresh-token",
  },

  todo: {
    category: "/api/todo/list",
    todo: "/api/todo/item",
  },

  journal: "/api/journal",
};
