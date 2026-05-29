import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { useAuthStore } from "../store/authStore";
import { getStats, getCards } from "../api/cards";
import type { Stats, Card } from "../types";
import LighthouseCardComp from "../components/LighthouseCard";

export default function DashboardPage() {
  const { user } = useAuthStore();
  const [stats, setStats] = useState<Stats | null>(null);
  const [recentCards, setRecentCards] = useState<Card[]>([]);
  const [loading, setLoading] = useState(true);
  const load = async () => {
    setLoading(true);
    try {
      const [s, cards] = await Promise.all([getStats(), getCards()]);
      setStats(s);
      setRecentCards(cards.slice(0, 8));
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center py-20 text-ocean-600">
        読み込み中...
      </div>
    );
  }

  return (
    <div className="max-w-5xl mx-auto px-4 py-8">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-800">
            ようこそ、{user?.username} さん
          </h1>
          <p className="text-gray-500 text-sm mt-0.5">あなたの灯台コレクション</p>
        </div>
        <Link
          to="/scan"
          className="flex items-center gap-2 px-4 py-2 bg-ocean-700 text-white rounded-lg font-medium hover:bg-ocean-800 transition-colors text-sm"
        >
          📷 QRスキャン
        </Link>
      </div>

      {/* 統計カード */}
      {stats && (
        <>
          <div className="grid grid-cols-3 gap-4 mb-8">
            <div className="bg-ocean-50 border border-ocean-200 rounded-xl p-4 text-center">
              <p className="text-3xl font-bold text-ocean-700">{stats.collected_count}</p>
              <p className="text-xs text-gray-500 mt-1">収集済みカード</p>
            </div>
            <div className="bg-gray-50 border border-gray-200 rounded-xl p-4 text-center">
              <p className="text-3xl font-bold text-gray-700">{stats.total_lighthouses}</p>
              <p className="text-xs text-gray-500 mt-1">総カード数</p>
            </div>
            <div className="bg-green-50 border border-green-200 rounded-xl p-4 text-center">
              <p className="text-3xl font-bold text-green-700">{stats.achievement_rate}%</p>
              <p className="text-xs text-gray-500 mt-1">達成率</p>
            </div>
          </div>

          {/* 達成率バー */}
          <div className="bg-white rounded-xl border border-gray-200 p-5 mb-8">
            <h2 className="font-bold text-gray-700 mb-4">地域別収集状況</h2>
            <div className="space-y-3">
              {stats.region_stats.map((r) => (
                <div key={r.region}>
                  <div className="flex justify-between text-sm mb-1">
                    <span className="text-gray-700">{r.region}</span>
                    <span className="text-gray-500">
                      {r.collected}/{r.total} ({r.rate}%)
                    </span>
                  </div>
                  <div className="h-2 bg-gray-100 rounded-full overflow-hidden">
                    <div
                      className="h-full bg-ocean-500 rounded-full transition-all"
                      style={{ width: `${r.rate}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>
        </>
      )}

      {/* 最近の収集 */}
      <div>
        <div className="flex items-center justify-between mb-4">
          <h2 className="font-bold text-gray-700">最近収集したカード</h2>
          <Link
            to="/lighthouses?collected=true"
            className="text-sm text-ocean-600 hover:underline"
          >
            すべて見る →
          </Link>
        </div>

        {recentCards.length === 0 ? (
          <div className="bg-white rounded-xl border border-gray-200 p-10 text-center text-gray-500">
            <p className="text-4xl mb-3">📷</p>
            <p className="font-medium">まだカードを収集していません</p>
            <p className="text-sm mt-1">灯台でQRコードをスキャンして最初のカードをゲットしよう！</p>
            <Link
              to="/scan"
              className="inline-block mt-4 px-5 py-2 bg-ocean-700 text-white rounded-lg text-sm font-medium hover:bg-ocean-800"
            >
              QRスキャンへ
            </Link>
          </div>
        ) : (
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
            {recentCards.map((card) =>
              card.lighthouse ? (
                <LighthouseCardComp
                  key={card.id}
                  lighthouse={{ ...card.lighthouse, is_collected: true }}
                />
              ) : null
            )}
          </div>
        )}
      </div>
    </div>
  );
}
