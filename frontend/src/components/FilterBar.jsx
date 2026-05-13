import { Search, X } from "lucide-react";

export default function FilterBar({
  search,
  onSearch,
  country,
  onCountry,
  specialty,
  onSpecialty,
  countries,
  specialties,
}) {
  const hasFilters = search || country || specialty;

  function clear() {
    onSearch("");
    onCountry("");
    onSpecialty("");
  }

  return (
    <div className="bg-white rounded-2xl border border-gray-100 p-4 flex flex-col sm:flex-row gap-3">
      <div className="relative flex-1">
        <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
        <input
          type="text"
          placeholder="Поиск университета..."
          value={search}
          onChange={(e) => onSearch(e.target.value)}
          className="w-full pl-9 pr-4 py-2.5 text-sm bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent placeholder-gray-400"
        />
      </div>

      <select
        value={country}
        onChange={(e) => onCountry(e.target.value)}
        className="sm:w-44 px-3 py-2.5 text-sm bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent text-gray-700"
      >
        <option value="">Все страны</option>
        {countries.map((c) => (
          <option key={c} value={c}>
            {c}
          </option>
        ))}
      </select>

      <select
        value={specialty}
        onChange={(e) => onSpecialty(e.target.value)}
        className="sm:w-52 px-3 py-2.5 text-sm bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent text-gray-700"
      >
        <option value="">Все специальности</option>
        {specialties.map((s) => (
          <option key={s.id} value={s.name}>
            {s.name}
          </option>
        ))}
      </select>

      {hasFilters && (
        <button
          onClick={clear}
          className="flex items-center gap-1.5 px-3 py-2.5 text-sm text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded-xl transition-colors"
        >
          <X size={14} />
          Сбросить
        </button>
      )}
    </div>
  );
}
