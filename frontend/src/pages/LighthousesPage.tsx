import { useEffect, useState, useCallback } from "react";
import { useSearchParams } from "react-router-dom";
import { getLighthouses } from "../api/lighthouses";
import { createCard, deleteCard } from "../api/cards";
import { useAuthStore } from "../store/authStore";
import type { Lighthouse } from "../types";
import LighthouseCardComp from "../components/LighthouseCard";

const REGIONS = [
  "北海道・東北",
  "関東・北陸・東海",
  "近畿・中国・四国",
  "九州・沖縄",
];

export default function LighthousesPage() {
  const { user } = useAuthStore();
  const [searchParams, setSearchParams] = useSearchParams();
  const [lighthouses, setLighthouses] = useState<Lighthouse[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [actionId, setActionId] = useState<number | null>(null);

  const region = searchParams.get("region") ?? "";
  const q = searchParams.get("q") ?? "";
  const collectedParam = searchParams.get("collected");

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const params: Record<string, string | boolean> = {};
      if (region) params.region = region;
      if (q) params.q = q;
      if (collectedParam === "true") params.collected = true;
      const res = await getLighthouses(params as Parameters<typeof getLighthouses>[0]);
      setLighthouses(res.items);
      setTotal(res.total);
    } finally {
      setLoading(false);
    }
  }, [region, q, collectedParam]);

  useEffect(() => {
    load();
  }, [load]);

  const handleCollect = async (id: number) => {
    setActionId(id);
    try {
      await createCard({ lighthouse_id: id });
      await load();
    } finally {
      setActionId(null);
    }
  };

  const handleRemove = async (id: number) => {
    setActionId(id);
    try {
      await deleteCard(id);
      await load();
    } finally {
      setActionId(null);
    }
  };

  const setParam = (key: string, value: string) => {
    const next = new URLSearchParams(searchParams);
    if (value) {
      next.set(key, value);
    } else {
      next.delete(key);
    }
    setSearchParams(next);
  };

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold text-gray-800 mb-6">灯台カード一覧</h1>

      {/* フィルター */}
      <div className="bg-white rounded-xl border border-gray-200 p-4 mb-6 flex flex-wrap gap-3">
        <input
          type="search"
          placeholder="灯台名で検索..."
          value={q}
          onChange={(e) => setParam("q", e.target.value)}
          className="border border-gray-300 rounded-lg px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-ocean-500 flex-1 min-w-48"
        />
        <select
          value={region}
          onChange={(e) => setParam("region", e.target.value)}
          className="border border-gray-300 rounded-lg px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-ocean-500"
        >
          <option value="">全地域</option>
          {REGIONS.map((r) => (
            <option key={r} value={r}>
              {r}
            </option>
          ))}
        </select>
        {user && (
          <select
            value={collectedParam ?? ""}
            onChange={(e) => setParam("collected", e.target.value)}
            className="border border-gray-300 rounded-lg px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-ocean-500"
          >
            <option value="">すべて</option>
            <option value="true">収集済みのみ</option>
            <option value="false">未収集のみ</option>
          </select>
        )}
      </div>

      <p className="text-sm text-gray-500 mb-4">{total} 件</p>

      {loading ? (
        <div className="text-center py-20 text-ocean-600">読み込み中...</div>
      ) : lighthouses.length === 0 ? (
        <div className="text-center py-20 text-gray-500">
          <p className="text-4xl mb-3">🔍</p>
          <p>該当する灯台が見つかりませんでした</p>
        </div>
      ) : (
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
          {lighthouses.map((lh) => (
            <LighthouseCardComp
              key={lh.id}
              lighthouse={lh}
              onCollect={user ? handleCollect : undefined}
              onRemove={user ? handleRemove : undefined}
              loading={actionId === lh.id}
            />
          ))}
        </div>
      )}
    </div>
  );
}
