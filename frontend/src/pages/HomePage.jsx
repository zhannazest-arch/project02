import { useState, useEffect, useCallback } from "react";
import { api } from "../api";
import FilterBar from "../components/FilterBar";
import UniversityCard from "../components/UniversityCard";
import Pagination from "../components/Pagination";
import { GraduationCap, Loader2 } from "lucide-react";

function useDebounce(value, delay) {
  const [debounced, setDebounced] = useState(value);
  useEffect(() => {
    const t = setTimeout(() => setDebounced(value), delay);
    return () => clearTimeout(t);
  }, [value, delay]);
  return debounced;
}

export default function HomePage() {
  const [search, setSearch] = useState("");
  const [country, setCountry] = useState("");
  const [specialty, setSpecialty] = useState("");
  const [page, setPage] = useState(1);

  const [universities, setUniversities] = useState([]);
  const [total, setTotal] = useState(0);
  const [pages, setPages] = useState(1);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const [countries, setCountries] = useState([]);
  const [specialties, setSpecialties] = useState([]);

  const debouncedSearch = useDebounce(search, 400);

  useEffect(() => {
    Promise.all([api.getCountries(), api.getSpecialties()]).then(([c, s]) => {
      setCountries(c);
      setSpecialties(s);
    });
  }, []);

  useEffect(() => {
    setPage(1);
  }, [debouncedSearch, country, specialty]);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setError(null);

    api
      .getUniversities({ search: debouncedSearch, country, specialty, page })
      .then((data) => {
        if (cancelled) return;
        setUniversities(data.items);
        setTotal(data.total);
        setPages(data.pages);
      })
      .catch(() => {
        if (!cancelled) setError("Не удалось загрузить данные.");
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });

    return () => {
      cancelled = true;
    };
  }, [debouncedSearch, country, specialty, page]);

  return (
    <main className="max-w-6xl mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Найдите свой университет
        </h1>
        <p className="text-gray-500">
          {total > 0 ? `${total} университетов в базе` : "Поиск по лучшим университетам мира"}
        </p>
      </div>

      <div className="mb-6">
        <FilterBar
          search={search}
          onSearch={setSearch}
          country={country}
          onCountry={setCountry}
          specialty={specialty}
          onSpecialty={setSpecialty}
          countries={countries}
          specialties={specialties}
        />
      </div>

      {error && (
        <div className="bg-red-50 border border-red-100 text-red-600 rounded-xl p-4 mb-6 text-sm">
          {error}
        </div>
      )}

      {loading ? (
        <div className="flex justify-center items-center py-24">
          <Loader2 size={32} className="animate-spin text-primary-500" />
        </div>
      ) : universities.length === 0 ? (
        <div className="flex flex-col items-center justify-center py-24 text-center">
          <GraduationCap size={48} className="text-gray-200 mb-4" />
          <p className="text-gray-500 text-lg font-medium">Ничего не найдено</p>
          <p className="text-gray-400 text-sm mt-1">Попробуйте изменить параметры поиска</p>
        </div>
      ) : (
        <>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5 mb-8">
            {universities.map((uni) => (
              <UniversityCard key={uni.id} university={uni} />
            ))}
          </div>

          <Pagination page={page} pages={pages} onChange={setPage} />
        </>
      )}
    </main>
  );
}
