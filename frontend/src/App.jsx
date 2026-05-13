import { Routes, Route } from "react-router-dom";
import Header from "./components/Header";
import ChatWidget from "./components/ChatWidget";
import HomePage from "./pages/HomePage";
import UniversityPage from "./pages/UniversityPage";

export default function App() {
  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/university/:id" element={<UniversityPage />} />
      </Routes>
      <ChatWidget />
    </div>
  );
}
