import { Link } from "react-router-dom";
import { useAuthStore } from "../store/authStore";

export default function TopPage() {
  const { user } = useAuthStore();

  return (
    <div className="min-h-[calc(100vh-120px)] flex flex-col">
      {/* ヒーロー */}
      <section className="bg-gradient-to-br from-ocean-800 via-ocean-700 to-ocean-600 text-white py-20 px-4 text-center flex-1 flex flex-col items-center justify-center">
        <div className="text-7xl mb-6">🏮</div>
        <h1 className="text-4xl sm:text-5xl font-bold mb-4">灯台カード収集帳</h1>
        <p className="text-lg sm:text-xl text-ocean-100 max-w-xl mx-auto mb-8">
          海上保安庁が管理する灯台カードDigitalの収集状況をデジタルで管理。
          QRコードをスキャンして、あなたのコレクションを記録しよう。
        </p>
        <div className="flex flex-col sm:flex-row gap-3 justify-center">
          {user ? (
            <>
              <Link
                to="/scan"
                className="px-8 py-3 bg-white text-ocean-800 rounded-full font-bold text-lg hover:bg-ocean-50 transition-colors shadow-lg"
              >
                QRをスキャン
              </Link>
              <Link
                to="/dashboard"
                className="px-8 py-3 border-2 border-white text-white rounded-full font-bold text-lg hover:bg-ocean-600 transition-colors"
              >
                マイページへ
              </Link>
            </>
          ) : (
            <>
              <Link
                to="/register"
                className="px-8 py-3 bg-white text-ocean-800 rounded-full font-bold text-lg hover:bg-ocean-50 transition-colors shadow-lg"
              >
                無料で始める
              </Link>
              <Link
                to="/lighthouses"
                className="px-8 py-3 border-2 border-white text-white rounded-full font-bold text-lg hover:bg-ocean-600 transition-colors"
              >
                灯台一覧を見る
              </Link>
            </>
          )}
        </div>
      </section>

      {/* 特徴 */}
      <section className="py-16 px-4 bg-white">
        <div className="max-w-5xl mx-auto">
          <h2 className="text-2xl font-bold text-center text-gray-800 mb-10">
            アプリの特徴
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-8">
            {[
              {
                icon: "📷",
                title: "QRコードで簡単登録",
                desc: "灯台に掲示されたQRコードをスキャンするだけ。現地で訪問した灯台をすぐに記録できます。",
              },
              {
                icon: "🗺️",
                title: "地図で収集状況を確認",
                desc: "全国の灯台を地図上に表示。収集済み・未収集を色分けして、次の目的地を計画しよう。",
              },
              {
                icon: "📊",
                title: "達成率で進捗管理",
                desc: "地域別の収集率や総達成率をダッシュボードで一目確認。コンプリートを目指そう！",
              },
            ].map((f) => (
              <div key={f.title} className="text-center">
                <div className="text-5xl mb-4">{f.icon}</div>
                <h3 className="text-lg font-bold text-gray-800 mb-2">{f.title}</h3>
                <p className="text-gray-600 text-sm leading-relaxed">{f.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      {!user && (
        <section className="bg-ocean-50 py-12 px-4 text-center">
          <h2 className="text-2xl font-bold text-ocean-800 mb-4">
            今すぐコレクションを始めよう
          </h2>
          <p className="text-gray-600 mb-6">
            無料でアカウント登録してすべての機能を使えます
          </p>
          <Link
            to="/register"
            className="inline-block px-10 py-3 bg-ocean-700 text-white rounded-full font-bold hover:bg-ocean-800 transition-colors"
          >
            新規登録（無料）
          </Link>
        </section>
      )}
    </div>
  );
}
