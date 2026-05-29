import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { useAuthStore } from "./store/authStore";
import Header from "./components/Header";
import TopPage from "./pages/TopPage";
import RegisterPage from "./pages/RegisterPage";
import LoginPage from "./pages/LoginPage";
import DashboardPage from "./pages/DashboardPage";
import LighthousesPage from "./pages/LighthousesPage";
import LighthouseDetailPage from "./pages/LighthouseDetailPage";
import ScanPage from "./pages/ScanPage";
import MapPage from "./pages/MapPage";

function RequireAuth({ children }: { children: React.ReactNode }) {
  const { user } = useAuthStore();
  return user ? <>{children}</> : <Navigate to="/login" replace />;
}

export default function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen flex flex-col">
        <Header />
        <main className="flex-1">
          <Routes>
            <Route path="/" element={<TopPage />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route
              path="/dashboard"
              element={
                <RequireAuth>
                  <DashboardPage />
                </RequireAuth>
              }
            />
            <Route path="/lighthouses" element={<LighthousesPage />} />
            <Route path="/lighthouses/:id" element={<LighthouseDetailPage />} />
            <Route
              path="/scan"
              element={
                <RequireAuth>
                  <ScanPage />
                </RequireAuth>
              }
            />
            <Route path="/map" element={<MapPage />} />
          </Routes>
        </main>
        <footer className="bg-ocean-900 text-white text-center py-6 text-xs space-y-2">
          <p className="font-medium text-sm">灯台カード収集帳</p>
          <p className="text-ocean-300">
            本アプリは海上保安庁の承認を得ていない非公式アプリです。海上保安庁とは一切関係ありません。
          </p>
          <p>
            <a
              href="https://www.kaiho.mlit.go.jp/info/kouhou/h17/k2005-09/k050908.htm"
              target="_blank"
              rel="noopener noreferrer"
              className="text-ocean-300 hover:text-white underline"
            >
              海上保安庁 海の安全情報・防犯対策
            </a>
            {" ｜ "}
            <a
              href="https://www.kaiho.mlit.go.jp/soshiki/koutsuu/toudai/card/index.html"
              target="_blank"
              rel="noopener noreferrer"
              className="text-ocean-300 hover:text-white underline"
            >
              灯台カードDigital（海上保安庁公式）
            </a>
          </p>
        </footer>
      </div>
    </BrowserRouter>
  );
}
