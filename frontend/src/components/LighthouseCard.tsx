import { Link } from "react-router-dom";
import type { Lighthouse } from "../types";

interface Props {
  lighthouse: Lighthouse;
}

export default function LighthouseCardComp({ lighthouse }: Props) {
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
          <div className="w-12 h-12 bg-ocean-300 rounded-full flex items-center justify-center">
            <span className="text-white text-xl font-bold">灯</span>
          </div>
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
      </div>
    </div>
  );
}
