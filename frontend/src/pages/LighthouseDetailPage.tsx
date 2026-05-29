import { useEffect, useState } from "react";
import { useParams, Link, useNavigate } from "react-router-dom";
import { getLighthouse } from "../api/lighthouses";
import { deleteCard, getCards, updateCard } from "../api/cards";
import { useAuthStore } from "../store/authStore";
import type { Lighthouse, Card } from "../types";

export default function LighthouseDetailPage() {
  const { id } = useParams<{ id: string }>();
  const { user } = useAuthStore();
  const navigate = useNavigate();
  const [lighthouse, setLighthouse] = useState<Lighthouse | null>(null);
  const [card, setCard] = useState<Card | null>(null);
  const [note, setNote] = useState("");
  const [editingNote, setEditingNote] = useState(false);
  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState(false);

  const load = async () => {
    if (!id) return;
    setLoading(true);
    try {
      const lh = await getLighthouse(Number(id));
      setLighthouse(lh);
      if (user) {
        const cards = await getCards();
        const found = cards.find((c) => c.lighthouse_id === lh.id) ?? null;
        setCard(found);
        setNote(found?.note ?? "");
      }
    } catch {
      navigate("/lighthouses");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, [id, user]);

  const handleRemove = async () => {
    if (!lighthouse) return;
    if (!confirm("収集記録を削除しますか？")) return;
    setActionLoading(true);
    try {
      await deleteCard(lighthouse.id);
      setCard(null);
      setLighthouse({ ...lighthouse, is_collected: false });
    } finally {
      setActionLoading(false);
    }
  };

  const handleSaveNote = async () => {
    if (!lighthouse || !card) return;
    setActionLoading(true);
    try {
      const updated = await updateCard(lighthouse.id, { note });
      setCard(updated);
      setEditingNote(false);
    } finally {
      setActionLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-20 text-ocean-600">
        読み込み中...
      </div>
    );
  }

  if (!lighthouse) return null;

  return (
    <div className="max-w-3xl mx-auto px-4 py-8">
      <Link to="/lighthouses" className="text-ocean-600 hover:underline text-sm mb-4 inline-block">
        ← 灯台一覧に戻る
      </Link>

      <div className="bg-white rounded-2xl shadow-md overflow-hidden">
        {/* カード画像 */}
        <div className="relative h-56 bg-gradient-to-br from-ocean-100 to-ocean-300 flex items-center justify-center">
          {lighthouse.card_image_url ? (
            <img
              src={lighthouse.card_image_url}
              alt={lighthouse.name}
              className="h-full w-full object-cover"
            />
          ) : (
            <div className="w-24 h-24 bg-ocean-300 rounded-full flex items-center justify-center">
              <span className="text-white text-4xl font-bold">灯</span>
            </div>
          )}
          {lighthouse.is_collected && (
            <div className="absolute top-3 right-3 bg-green-500 text-white text-sm font-bold px-3 py-1 rounded-full">
              ✓ 収集済み
            </div>
          )}
          {lighthouse.is_climbable && (
            <div className="absolute top-3 left-3 bg-amber-500 text-white text-sm font-bold px-3 py-1 rounded-full">
              登れる灯台
            </div>
          )}
        </div>

        <div className="p-6">
          <h1 className="text-2xl font-bold text-gray-800">{lighthouse.name}</h1>
          {lighthouse.name_kana && (
            <p className="text-gray-400 text-sm mt-0.5">{lighthouse.name_kana}</p>
          )}

          <div className="flex flex-wrap gap-2 mt-3">
            <span className="bg-ocean-100 text-ocean-700 text-xs px-2 py-0.5 rounded-full">
              {lighthouse.region}
            </span>
            <span className="bg-gray-100 text-gray-600 text-xs px-2 py-0.5 rounded-full">
              {lighthouse.prefecture}
            </span>
            {lighthouse.established_year && (
              <span className="bg-gray-100 text-gray-600 text-xs px-2 py-0.5 rounded-full">
                {lighthouse.established_year}年初点灯
              </span>
            )}
          </div>

          {lighthouse.description && (
            <p className="mt-4 text-gray-600 text-sm leading-relaxed">
              {lighthouse.description}
            </p>
          )}

          {/* 座標 */}
          {lighthouse.latitude != null && lighthouse.longitude != null && (
            <p className="mt-3 text-xs text-gray-400">
              📍 {lighthouse.latitude.toFixed(4)}, {lighthouse.longitude.toFixed(4)}
            </p>
          )}

          {/* 海保リンク */}
          {lighthouse.jcg_page_url && (
            <a
              href={lighthouse.jcg_page_url}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-block mt-3 text-xs text-ocean-600 hover:underline"
            >
              🔗 海上保安庁の灯台ページ
            </a>
          )}

          {/* 収集アクション */}
          {user ? (
            <div className="mt-6 border-t pt-4">
              {lighthouse.is_collected ? (
                <>
                  <div className="flex items-center gap-3">
                    <p className="text-sm text-green-600 font-medium">
                      ✓ 収集済み（
                      {card &&
                        new Date(card.collected_at).toLocaleDateString("ja-JP")}
                      ）
                    </p>
                    <button
                      onClick={handleRemove}
                      disabled={actionLoading}
                      className="text-xs text-red-500 hover:underline disabled:opacity-50"
                    >
                      収集を取消
                    </button>
                  </div>

                  {/* メモ */}
                  <div className="mt-3">
                    <p className="text-xs font-medium text-gray-500 mb-1">メモ</p>
                    {editingNote ? (
                      <div className="flex gap-2">
                        <textarea
                          value={note}
                          onChange={(e) => setNote(e.target.value)}
                          rows={3}
                          className="flex-1 border border-gray-300 rounded-lg px-2 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-ocean-500"
                          placeholder="訪問時の感想など..."
                        />
                        <div className="flex flex-col gap-1">
                          <button
                            onClick={handleSaveNote}
                            disabled={actionLoading}
                            className="px-3 py-1 bg-ocean-600 text-white text-xs rounded hover:bg-ocean-700 disabled:opacity-50"
                          >
                            保存
                          </button>
                          <button
                            onClick={() => {
                              setEditingNote(false);
                              setNote(card?.note ?? "");
                            }}
                            className="px-3 py-1 border text-xs rounded hover:bg-gray-50"
                          >
                            キャンセル
                          </button>
                        </div>
                      </div>
                    ) : (
                      <div
                        onClick={() => setEditingNote(true)}
                        className="cursor-pointer min-h-[2rem] p-2 rounded border border-dashed border-gray-300 text-sm text-gray-600 hover:border-ocean-400 hover:bg-ocean-50 transition-colors"
                      >
                        {card?.note || (
                          <span className="text-gray-400">クリックしてメモを追加...</span>
                        )}
                      </div>
                    )}
                  </div>
                </>
              ) : (
                <p className="text-sm text-gray-500 mt-4">
                  灯台カードのQRコードをスキャンして収集できます。
                </p>
              )}
            </div>
          ) : (
            <div className="mt-6 border-t pt-4 text-center">
              <p className="text-sm text-gray-500 mb-3">
                収集記録を管理するにはログインが必要です
              </p>
              <Link
                to="/login"
                className="inline-block px-6 py-2 bg-ocean-700 text-white rounded-lg text-sm font-medium hover:bg-ocean-800"
              >
                ログイン
              </Link>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
