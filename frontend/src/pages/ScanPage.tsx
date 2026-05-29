import { useEffect, useRef, useState } from "react";
import { Html5Qrcode } from "html5-qrcode";
import { identifyByUrl } from "../api/lighthouses";
import { createCard } from "../api/cards";
import type { Lighthouse } from "../types";
import { Link } from "react-router-dom";

type ScanState = "idle" | "scanning" | "found" | "not_found" | "card_not_registered" | "collected";

export default function ScanPage() {
  const scannerRef = useRef<Html5Qrcode | null>(null);
  const [scanState, setScanState] = useState<ScanState>("idle");
  const [found, setFound] = useState<Lighthouse | null>(null);
  const [error, setError] = useState("");
  const [actionLoading, setActionLoading] = useState(false);

  const stopScanner = async () => {
    if (scannerRef.current) {
      try {
        await scannerRef.current.stop();
      } catch {
        // ignore
      }
      scannerRef.current = null;
    }
  };

  const startScanner = async () => {
    setScanState("scanning");
    setError("");
    setFound(null);

    await stopScanner();

    const scanner = new Html5Qrcode("qr-reader");
    scannerRef.current = scanner;

    try {
      await scanner.start(
        { facingMode: "environment" },
        { fps: 10, qrbox: { width: 250, height: 250 } },
        async (decodedText) => {
          await stopScanner();
          await handleUrl(decodedText);
        },
        () => {}
      );
    } catch {
      setError("カメラへのアクセスが拒否されました。ブラウザの設定を確認してください。");
      setScanState("idle");
    }
  };

  const handleUrl = async (url: string) => {
    try {
      const lh = await identifyByUrl(url);
      setFound(lh);
      setScanState("found");
    } catch (err: unknown) {
      const detail =
        (err as { response?: { data?: { detail?: string } } })?.response?.data?.detail;
      if (detail === "LIGHTHOUSE_CARD_NOT_REGISTERED") {
        setScanState("card_not_registered");
      } else {
        setScanState("not_found");
      }
    }
  };

  const handleCollect = async () => {
    if (!found) return;
    setActionLoading(true);
    try {
      await createCard({ lighthouse_id: found.id });
      setScanState("collected");
    } catch (err: unknown) {
      const msg =
        (err as { response?: { data?: { detail?: string } } })?.response?.data
          ?.detail ?? "登録に失敗しました";
      setError(msg);
    } finally {
      setActionLoading(false);
    }
  };

  const reset = () => {
    setScanState("idle");
    setFound(null);
    setError("");
  };

  useEffect(() => {
    return () => {
      stopScanner();
    };
  }, []);

  return (
    <div className="max-w-xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold text-gray-800 mb-2">QRコードスキャン</h1>
      <p className="text-gray-500 text-sm mb-6">
        灯台に掲示されているQRコードをカメラで読み取ってください
      </p>

      {error && (
        <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
          {error}
        </div>
      )}

      {/* スキャン完了 */}
      {scanState === "collected" && found && (
        <div className="bg-green-50 border-2 border-green-400 rounded-2xl p-6 text-center">
          <div className="text-5xl mb-3">🎉</div>
          <h2 className="text-xl font-bold text-green-800 mb-1">収集完了！</h2>
          <p className="text-green-700 font-medium">{found.name}</p>
          <p className="text-green-600 text-sm mt-1">{found.prefecture}</p>
          <div className="flex gap-3 mt-4 justify-center">
            <button
              onClick={reset}
              className="px-5 py-2 border-2 border-green-500 text-green-700 rounded-lg text-sm font-medium hover:bg-green-50"
            >
              続けてスキャン
            </button>
            <Link
              to="/dashboard"
              className="px-5 py-2 bg-green-600 text-white rounded-lg text-sm font-medium hover:bg-green-700"
            >
              マイページへ
            </Link>
          </div>
        </div>
      )}

      {/* 灯台が見つかった */}
      {scanState === "found" && found && (
        <div className="bg-white border-2 border-ocean-400 rounded-2xl p-6">
          <div className="text-center mb-4">
            <h2 className="text-lg font-bold text-gray-800">灯台が見つかりました！</h2>
          </div>
          <div className="bg-ocean-50 rounded-xl p-4 mb-4">
            <p className="font-bold text-ocean-800 text-lg">{found.name}</p>
            {found.name_kana && (
              <p className="text-ocean-600 text-sm">{found.name_kana}</p>
            )}
            <p className="text-gray-600 text-sm mt-1">
              {found.prefecture} / {found.region}
            </p>
            {found.is_collected && (
              <p className="text-green-600 text-sm mt-1 font-medium">✓ すでに収集済みです</p>
            )}
          </div>
          {found.is_collected ? (
            <div className="flex gap-3">
              <button onClick={reset} className="flex-1 py-2 border rounded-lg text-sm">
                戻る
              </button>
              <Link
                to={`/lighthouses/${found.id}`}
                className="flex-1 py-2 bg-ocean-600 text-white rounded-lg text-sm font-medium text-center hover:bg-ocean-700"
              >
                詳細を見る
              </Link>
            </div>
          ) : (
            <div className="flex gap-3">
              <button onClick={reset} className="flex-1 py-2 border rounded-lg text-sm">
                キャンセル
              </button>
              <button
                onClick={handleCollect}
                disabled={actionLoading}
                className="flex-1 py-2 bg-ocean-700 text-white rounded-lg text-sm font-bold hover:bg-ocean-800 disabled:opacity-50"
              >
                {actionLoading ? "登録中..." : "コレクションに追加"}
              </button>
            </div>
          )}
        </div>
      )}

      {/* 海保QRだがDB未登録 */}
      {scanState === "card_not_registered" && (
        <div className="bg-blue-50 border border-blue-300 rounded-2xl p-6 text-center mb-4">
          <p className="text-blue-800 font-medium">灯台カードのQRコードを検出しました</p>
          <p className="text-blue-600 text-sm mt-1">
            このQRコードはまだデータベースに登録されていません。
            <br />引き続き他の灯台のQRコードをスキャンしてください。
          </p>
          <button
            onClick={reset}
            className="mt-4 px-5 py-2 border border-blue-400 text-blue-700 rounded-lg text-sm hover:bg-blue-50"
          >
            再スキャン
          </button>
        </div>
      )}

      {/* QRコード見つからず（灯台カード以外） */}
      {scanState === "not_found" && (
        <div className="bg-amber-50 border border-amber-200 rounded-2xl p-6 text-center mb-4">
          <div className="text-4xl mb-2">🔍</div>
          <p className="text-amber-800 font-medium">対応する灯台が見つかりませんでした</p>
          <p className="text-amber-600 text-sm mt-1">
            このQRコードは灯台カード用ではない可能性があります
          </p>
          <button
            onClick={reset}
            className="mt-4 px-5 py-2 border border-amber-400 text-amber-700 rounded-lg text-sm hover:bg-amber-50"
          >
            再試行
          </button>
        </div>
      )}

      {/* スキャナー */}
      {(scanState === "idle" || scanState === "scanning") && (
        <>
          <div
            id="qr-reader"
            className={`w-full rounded-2xl overflow-hidden border-2 border-gray-200 mb-4 ${
              scanState !== "scanning" ? "hidden" : ""
            }`}
          />

          {scanState === "idle" && (
            <button
              onClick={startScanner}
              className="w-full py-4 bg-ocean-700 text-white rounded-2xl font-bold text-lg hover:bg-ocean-800 transition-colors flex items-center justify-center gap-2 mb-6"
            >
              <span>📷</span> カメラを起動してスキャン
            </button>
          )}

          {scanState === "scanning" && (
            <button
              onClick={async () => {
                await stopScanner();
                setScanState("idle");
              }}
              className="w-full py-2 border border-gray-300 text-gray-600 rounded-xl text-sm hover:bg-gray-50 mb-6"
            >
              スキャンを停止
            </button>
          )}
        </>
      )}
    </div>
  );
}
