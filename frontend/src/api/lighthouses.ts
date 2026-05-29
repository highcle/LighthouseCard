import client from "./client";
import type { Lighthouse, LighthouseListResponse } from "../types";

export const getLighthouses = (params?: {
  region?: string;
  prefecture?: string;
  q?: string;
  collected?: boolean;
}) =>
  client
    .get<LighthouseListResponse>("/lighthouses", { params })
    .then((r) => r.data);

export const getLighthouse = (id: number) =>
  client.get<Lighthouse>(`/lighthouses/${id}`).then((r) => r.data);

export const identifyByUrl = (url: string) =>
  client
    .post<Lighthouse>("/lighthouses/identify-by-url", { url })
    .then((r) => r.data);

export const registerFromQr = (data: { name: string; qr_code_url: string }) =>
  client
    .post<Lighthouse>("/lighthouses/register-from-qr", data)
    .then((r) => r.data);
