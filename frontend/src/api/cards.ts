import client from "./client";
import type { Card, Stats } from "../types";

export const getCards = () =>
  client.get<Card[]>("/cards").then((r) => r.data);

export const createCard = (data: { lighthouse_id: number; note?: string }) =>
  client.post<Card>("/cards", data).then((r) => r.data);

export const updateCard = (lighthouseId: number, data: { note: string }) =>
  client.patch<Card>(`/cards/${lighthouseId}`, data).then((r) => r.data);

export const deleteCard = (lighthouseId: number) =>
  client.delete(`/cards/${lighthouseId}`);

export const getStats = () =>
  client.get<Stats>("/cards/stats").then((r) => r.data);
