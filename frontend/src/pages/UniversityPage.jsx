import { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";
import {
  ArrowLeft,
  MapPin,
  Trophy,
  Calendar,
  Users,
  DollarSign,
  ExternalLink,
  Loader2,
  GraduationCap,
  ClipboardList,
  Languages,
  Star,
  CheckCircle2,
} from "lucide-react";
import { api } from "../api";

function StatCard({ icon: Icon, label, value, color = "text-gray-700" }) {
  if (!value) return null;
  return (
    <div className="bg-white rounded-2xl border border-gray-100 p-4 flex items-center gap-4">
      <div className="w-10 h-10 rounded-xl bg-gray-50 flex items-center justify-center flex-shrink-0">
        <Icon size={18} className={color} />
      </div>
      <div>
        <p className="text-xs text-gray-500 font-medium">{label}</p>
        <p className="text-sm font-semibold text-gray-900 mt-0.5">{value}</p>
      </div>
    </div>
  );
}

function AdmissionSection({ admission }) {
  if (!admission) return null;

  return (
    <div className="bg-white rounded-2xl border border-gray-100 p-6 space-y-5">
      <div className="flex items-center gap-2">
        <ClipboardList size={18} className="text-primary-600" />
        <h2 className="text-lg font-semibold text-gray-900">Требования к поступлению</h2>
      </div>

      {admission.description && (
        <p className="text-sm text-gray-600 leading-relaxed">{admission.description}</p>
      )}

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
        {admission.min_gpa != null && (
          <div className="flex items-start gap-3 p-3 bg-amber-50 rounded-xl">
            <Star size={16} className="text-amber-500 mt-0.5 flex-shrink-0" />
            <div>
              <p className="text-xs font-medium text-amber-700">Минимальный GPA</p>
              <p className="text-sm font-bold text-amber-900">{admission.min_gpa.toFixed(1)} / 4.0</p>
            </div>
          </div>
        )}
        {admission.language_requirement && (
          <div className="flex items-start gap-3 p-3 bg-blue-50 rounded-xl">
            <Languages size={16} className="text-blue-500 mt-0.5 flex-shrink-0" />
            <div>
              <p className="text-xs font-medium text-blue-700">Языковые требования</p>
              <p className="text-sm text-blue-900">{admission.language_requirement}</p>
            </div>
          </div>
        )}
      </div>

      {admission.exams?.length > 0 && (
        <div>
          <p className="text-sm font-semibold text-gray-700 mb-3">Необходимые экзамены</p>
          <div className="space-y-2">
            {admission.exams.map((exam) => (
              <div
                key={exam.id}
                className="flex items-center justify-between gap-4 px-4 py-3 bg-gray-50 rounded-xl hover:bg-gray-100 transition-colors"
              >
                <div className="flex items-center gap-2 min-w-0">
                  <CheckCircle2 size={15} className="text-primary-500 flex-shrink-0" />
                  <div className="min-w-0">
                    <span className="text-sm font-medium text-gray-900">{exam.exam_name}</span>
                    {exam.notes && (
                      <p className="text-xs text-gray-500 mt-0.5 truncate">{exam.notes}</p>
                    )}
                  </div>
                </div>
                {exam.min_score && (
                  <div className="flex-shrink-0 text-right">
                    <span className="text-xs text-gray-500">мин.</span>
                    <span className="ml-1 text-sm font-bold text-primary-700">{exam.min_score}</span>
                    {exam.max_score && (
                      <span className="text-xs text-gray-400"> / {exam.max_score}</span>
                    )}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default function UniversityPage() {
  const { id } = useParams();
  const [university, setUniversity] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true);
    api
      .getUniversity(id)
      .then(setUniversity)
      .catch(() => setError("Университет не найден."))
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-[60vh]">
        <Loader2 size={32} className="animate-spin text-primary-500" />
      </div>
    );
  }

  if (error || !university) {
    return (
      <div className="max-w-6xl mx-auto px-4 py-16 flex flex-col items-center gap-4">
        <GraduationCap size={48} className="text-gray-200" />
        <p className="text-gray-500">{error || "Не найдено"}</p>
        <Link
          to="/"
          className="flex items-center gap-2 text-primary-600 hover:text-primary-700 text-sm font-medium"
        >
          <ArrowLeft size={16} />
          На главную
        </Link>
      </div>
    );
  }

  const {
    name, country, city, description, image_url, website,
    ranking, founded_year, tuition_min, tuition_max,
    students_count, specialties, admission,
  } = university;

  const tuition =
    tuition_min != null
      ? tuition_min === 0
        ? "Бесплатно"
        : `$${tuition_min.toLocaleString()}${tuition_max ? `–$${tuition_max.toLocaleString()}` : "+"} / год`
      : null;

  return (
    <main className="max-w-6xl mx-auto px-4 py-8">
      <Link
        to="/"
        className="inline-flex items-center gap-2 text-gray-500 hover:text-gray-700 text-sm font-medium mb-6 transition-colors"
      >
        <ArrowLeft size={16} />
        Назад
      </Link>

      <div className="relative rounded-3xl overflow-hidden h-64 bg-gray-100 mb-8">
        {image_url ? (
          <img src={image_url} alt={name} className="w-full h-full object-cover" />
        ) : (
          <div className="w-full h-full bg-gradient-to-br from-primary-100 to-primary-50 flex items-center justify-center">
            <span className="text-8xl font-bold text-primary-200">{name[0]}</span>
          </div>
        )}
        <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent" />
        <div className="absolute bottom-6 left-6 right-6">
          <div className="flex items-end justify-between gap-4">
            <div>
              <h1 className="text-2xl sm:text-3xl font-bold text-white leading-tight">{name}</h1>
              <div className="flex items-center gap-1.5 text-white/80 text-sm mt-1">
                <MapPin size={14} />
                {city}, {country}
              </div>
            </div>
            {ranking && (
              <div className="flex items-center gap-1.5 bg-white/90 backdrop-blur px-3 py-1.5 rounded-full text-sm font-bold text-amber-600 flex-shrink-0">
                <Trophy size={14} />
                #{ranking} в мире
              </div>
            )}
          </div>
        </div>
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-8">
        <StatCard icon={Trophy} label="Мировой рейтинг" value={ranking ? `#${ranking}` : null} color="text-amber-500" />
        <StatCard icon={Calendar} label="Год основания" value={founded_year?.toString()} color="text-blue-500" />
        <StatCard icon={DollarSign} label="Стоимость обучения" value={tuition} color="text-green-500" />
        <StatCard icon={Users} label="Студентов" value={students_count?.toLocaleString()} color="text-purple-500" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          {description && (
            <div className="bg-white rounded-2xl border border-gray-100 p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-3">Об университете</h2>
              <p className="text-gray-600 leading-relaxed text-sm">{description}</p>
            </div>
          )}

          <AdmissionSection admission={admission} />

          {specialties.length > 0 && (
            <div className="bg-white rounded-2xl border border-gray-100 p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">Специальности</h2>
              <div className="flex flex-wrap gap-2">
                {specialties.map((s) => (
                  <Link
                    key={s.id}
                    to={`/?specialty=${encodeURIComponent(s.name)}`}
                    className="px-3 py-1.5 bg-primary-50 hover:bg-primary-100 text-primary-700 rounded-lg text-sm font-medium transition-colors"
                  >
                    {s.name}
                  </Link>
                ))}
              </div>
            </div>
          )}
        </div>

        <div className="space-y-4">
          {website && (
            <a
              href={website}
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center justify-center gap-2 w-full px-4 py-3 bg-primary-600 hover:bg-primary-700 text-white rounded-2xl text-sm font-semibold transition-colors"
            >
              <ExternalLink size={16} />
              Официальный сайт
            </a>
          )}

          <div className="bg-white rounded-2xl border border-gray-100 p-5">
            <h3 className="text-sm font-semibold text-gray-900 mb-4">Информация</h3>
            <div className="space-y-3">
              <div className="flex items-center justify-between text-sm">
                <span className="text-gray-500">Страна</span>
                <span className="font-medium text-gray-900">{country}</span>
              </div>
              <div className="flex items-center justify-between text-sm">
                <span className="text-gray-500">Город</span>
                <span className="font-medium text-gray-900">{city}</span>
              </div>
              {founded_year && (
                <div className="flex items-center justify-between text-sm">
                  <span className="text-gray-500">Основан</span>
                  <span className="font-medium text-gray-900">{founded_year}</span>
                </div>
              )}
              {students_count && (
                <div className="flex items-center justify-between text-sm">
                  <span className="text-gray-500">Студентов</span>
                  <span className="font-medium text-gray-900">{students_count.toLocaleString()}</span>
                </div>
              )}
              {tuition && (
                <div className="flex items-center justify-between text-sm">
                  <span className="text-gray-500">Стоимость</span>
                  <span className="font-medium text-green-600">{tuition}</span>
                </div>
              )}
            </div>
          </div>

          <Link
            to={`/?country=${encodeURIComponent(country)}`}
            className="flex items-center justify-center gap-2 w-full px-4 py-3 bg-gray-50 hover:bg-gray-100 text-gray-700 rounded-2xl text-sm font-medium transition-colors border border-gray-100"
          >
            <MapPin size={15} />
            Другие университеты в {country}
          </Link>
        </div>
      </div>
    </main>
  );
}
