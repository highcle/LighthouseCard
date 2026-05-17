import { Link } from "react-router-dom";
import type { Lighthouse } from "../types";

interface Props {
  lighthouse: Lighthouse;
  onCollect?: (id: number) => void;
  onRemove?: (id: number) => void;
  loading?: boolean;
}

export default function LighthouseCardComp({
  lighthouse,
  onCollect,
  onRemove,
  loading,
}: Props) {
  const collected = lighthouse.is_collected;

  return (
    <div
      className={`rounded-xl border-2 overflow-hidden shadow-sm hover:shadow-md transition-shadow bg-white flex flex-col ${
        collected ? "border-green-400" : "border-gray-200"
      }`}
    >
      {/* カード画像エリア */}
      <div className="relative aspect-[3/2] bg-gradient-to-br from-ocean-100 to-ocean-200 flex items-center justify-center overflow-hidden">
        {lighthouse.card_image_url ? (
          <img
            src={lighthouse.card_image_url}
            alt={lighthouse.name}
            className="w-full h-full object-cover"
          />
        ) : (
          <span className="text-5xl">🏮</span>
        )}
        {collected && (
          <div className="absolute top-2 right-2 bg-green-500 text-white text-xs font-bold px-2 py-0.5 rounded-full">
            収集済み
          </div>
        )}
        {lighthouse.is_climbable && (
          <div className="absolute top-2 left-2 bg-amber-500 text-white text-xs font-bold px-2 py-0.5 rounded-full">
            登れる
          </div>
        )}
      </div>

      {/* 情報エリア */}
      <div className="p-3 flex-1 flex flex-col">
        <Link
          to={`/lighthouses/${lighthouse.id}`}
          className="font-bold text-ocean-800 hover:text-ocean-600 hover:underline leading-tight"
        >
          {lighthouse.name}
        </Link>
        <p className="text-xs text-gray-500 mt-0.5">
          {lighthouse.prefecture} / {lighthouse.region}
        </p>
        {lighthouse.established_year && (
          <p className="text-xs text-gray-400 mt-0.5">
            {lighthouse.established_year}年初点灯
          </p>
        )}

        {(onCollect || onRemove) && (
          <div className="mt-auto pt-2">
            {collected ? (
              <button
                onClick={() => onRemove?.(lighthouse.id)}
                disabled={loading}
                className="w-full text-xs py-1.5 px-3 rounded border border-red-300 text-red-600 hover:bg-red-50 transition-colors disabled:opacity-50"
              >
                収集を取消
              </button>
            ) : (
              <button
                onClick={() => onCollect?.(lighthouse.id)}
                disabled={loading}
                className="w-full text-xs py-1.5 px-3 rounded bg-ocean-600 text-white hover:bg-ocean-700 transition-colors disabled:opacity-50"
              >
                収集済みにする
              </button>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
