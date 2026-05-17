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
