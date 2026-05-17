import { Link, useNavigate } from "react-router-dom";
import { useAuthStore } from "../store/authStore";

export default function Header() {
  const { user, clearAuth } = useAuthStore();
  const navigate = useNavigate();

  const handleLogout = () => {
    clearAuth();
    navigate("/");
  };

  return (
    <header className="bg-ocean-800 text-white shadow-md">
      <div className="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between">
        <Link to="/" className="flex items-center gap-2 text-xl font-bold hover:opacity-90">
          <span className="text-2xl">🏮</span>
          <span>灯台カード収集帳</span>
        </Link>
        <nav className="flex items-center gap-1 sm:gap-3 text-sm">
          <Link
            to="/lighthouses"
            className="px-2 py-1 rounded hover:bg-ocean-700 transition-colors"
          >
            灯台一覧
          </Link>
          <Link
            to="/map"
            className="px-2 py-1 rounded hover:bg-ocean-700 transition-colors"
          >
            地図
          </Link>
          {user ? (
            <>
              <Link
                to="/scan"
                className="px-2 py-1 rounded bg-ocean-500 hover:bg-ocean-400 transition-colors font-medium"
              >
                QRスキャン
              </Link>
              <Link
                to="/dashboard"
                className="px-2 py-1 rounded hover:bg-ocean-700 transition-colors"
              >
                マイページ
              </Link>
              <button
                onClick={handleLogout}
                className="px-2 py-1 rounded hover:bg-ocean-700 transition-colors text-gray-300 hover:text-white"
              >
                ログアウト
              </button>
            </>
          ) : (
            <>
              <Link
                to="/login"
                className="px-2 py-1 rounded hover:bg-ocean-700 transition-colors"
              >
                ログイン
              </Link>
              <Link
                to="/register"
                className="px-3 py-1 rounded bg-ocean-500 hover:bg-ocean-400 transition-colors font-medium"
              >
                新規登録
              </Link>
            </>
          )}
        </nav>
      </div>
    </header>
  );
}
