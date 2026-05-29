import client from "./client";
import type { TokenResponse, User } from "../types";

export const register = (data: {
  username: string;
  password: string;
}) => client.post<TokenResponse>("/auth/register", data).then((r) => r.data);

export const login = (data: { username: string; password: string }) =>
  client.post<TokenResponse>("/auth/login", data).then((r) => r.data);

export const getMe = () => client.get<User>("/auth/me").then((r) => r.data);
