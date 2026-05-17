import { useEffect, useState } from "react";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import { getLighthouses } from "../api/lighthouses";
import { Link } from "react-router-dom";
import type { Lighthouse } from "../types";
import { useAuthStore } from "../store/authStore";

// デフォルトアイコン修正
delete (L.Icon.Default.prototype as unknown as Record<string, unknown>)._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png",
  iconUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
  shadowUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
});

const collectedIcon = new L.Icon({
  iconUrl: "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png",
  shadowUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41],
});

const defaultIcon = new L.Icon({
  iconUrl: "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-grey.png",
  shadowUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41],
});

export default function MapPage() {
  const { user } = useAuthStore();
  const [lighthouses, setLighthouses] = useState<Lighthouse[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getLighthouses()
      .then((res) => setLighthouses(res.items))
      .finally(() => setLoading(false));
  }, []);

  const collected = lighthouses.filter((lh) => lh.is_collected).length;

  return (
    <div className="h-[calc(100vh-120px)] flex flex-col">
      {/* 凡例バー */}
      <div className="bg-white border-b border-gray-200 px-4 py-2 flex items-center gap-6 text-sm flex-shrink-0">
        <span className="font-medium text-gray-700">灯台マップ</span>
        <span className="flex items-center gap-1.5">
          <span className="w-3 h-3 rounded-full bg-green-500 inline-block" />
          収集済み {user ? `(${collected}件)` : ""}
        </span>
        <span className="flex items-center gap-1.5">
          <span className="w-3 h-3 rounded-full bg-gray-400 inline-block" />
          未収集
        </span>
        <span className="text-gray-400 ml-auto">全 {lighthouses.length} 灯台</span>
      </div>

      {loading ? (
        <div className="flex-1 flex items-center justify-center text-ocean-600">
          地図を読み込み中...
        </div>
      ) : (
        <MapContainer
          center={[36.5, 136.0]}
          zoom={5}
          className="flex-1"
          style={{ zIndex: 0 }}
        >
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          {lighthouses.map((lh) => (
            <Marker
              key={lh.id}
              position={[lh.latitude, lh.longitude]}
              icon={lh.is_collected ? collectedIcon : defaultIcon}
            >
              <Popup>
                <div className="text-sm min-w-40">
                  <p className="font-bold text-gray-800">{lh.name}</p>
                  <p className="text-gray-500 text-xs">{lh.prefecture}</p>
                  {lh.is_collected && (
                    <p className="text-green-600 text-xs mt-0.5 font-medium">✓ 収集済み</p>
                  )}
                  {lh.is_climbable && (
                    <p className="text-amber-600 text-xs mt-0.5">登れる灯台</p>
                  )}
                  <Link
                    to={`/lighthouses/${lh.id}`}
                    className="text-ocean-600 text-xs hover:underline mt-1 block"
                  >
                    詳細を見る →
                  </Link>
                </div>
              </Popup>
            </Marker>
          ))}
        </MapContainer>
      )}
    </div>
  );
}
