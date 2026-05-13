import { Link, useLocation } from "react-router-dom";
import { GraduationCap } from "lucide-react";

export default function Header() {
  const { pathname } = useLocation();

  return (
    <header className="sticky top-0 z-40 bg-white/80 backdrop-blur border-b border-gray-100">
      <div className="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
        <Link to="/" className="flex items-center gap-2 font-semibold text-gray-900 hover:text-primary-600 transition-colors">
          <div className="w-8 h-8 bg-primary-600 rounded-lg flex items-center justify-center">
            <GraduationCap size={18} className="text-white" />
          </div>
          <span className="text-lg">UniSearch</span>
        </Link>

        <nav className="flex items-center gap-1">
          <Link
            to="/"
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
              pathname === "/"
                ? "bg-primary-50 text-primary-700"
                : "text-gray-600 hover:text-gray-900 hover:bg-gray-100"
            }`}
          >
            Университеты
          </Link>
        </nav>
      </div>
    </header>
  );
}
