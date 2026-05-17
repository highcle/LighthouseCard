import { create } from "zustand";
import type { User } from "../types";

interface AuthState {
  user: User | null;
  token: string | null;
  setAuth: (user: User, token: string) => void;
  clearAuth: () => void;
}

const savedUser = localStorage.getItem("user");
const savedToken = localStorage.getItem("access_token");

export const useAuthStore = create<AuthState>((set) => ({
  user: savedUser ? (JSON.parse(savedUser) as User) : null,
  token: savedToken,
  setAuth: (user, token) => {
    localStorage.setItem("user", JSON.stringify(user));
    localStorage.setItem("access_token", token);
    set({ user, token });
  },
  clearAuth: () => {
    localStorage.removeItem("user");
    localStorage.removeItem("access_token");
    set({ user: null, token: null });
  },
}));
