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
        <footer className="bg-ocean-900 text-white text-center py-4 text-sm">
          <p>灯台カード収集帳 — 海上保安庁の灯台カードDigitalを管理するアプリ</p>
        </footer>
      </div>
    </BrowserRouter>
  );
}
