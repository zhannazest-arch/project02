import { Link } from "react-router-dom";
import { MapPin, Trophy, Users, DollarSign } from "lucide-react";

function SpecialtyBadge({ name }) {
  return (
    <span className="inline-flex items-center px-2 py-0.5 rounded-md bg-primary-50 text-primary-700 text-xs font-medium">
      {name}
    </span>
  );
}

export default function UniversityCard({ university }) {
  const { id, name, country, city, ranking, image_url, tuition_min, tuition_max, students_count, specialties } =
    university;

  const tuition =
    tuition_min != null
      ? tuition_min === 0
        ? "Бесплатно"
        : `$${tuition_min.toLocaleString()}${tuition_max ? `–$${tuition_max.toLocaleString()}` : "+"}/год`
      : null;

  return (
    <Link
      to={`/university/${id}`}
      className="group bg-white rounded-2xl border border-gray-100 overflow-hidden hover:shadow-md hover:border-primary-100 transition-all duration-200 flex flex-col"
    >
      <div className="relative h-44 overflow-hidden bg-gray-100">
        {image_url ? (
          <img
            src={image_url}
            alt={name}
            className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
            loading="lazy"
          />
        ) : (
          <div className="w-full h-full bg-gradient-to-br from-primary-100 to-primary-50 flex items-center justify-center">
            <span className="text-4xl font-bold text-primary-300">{name[0]}</span>
          </div>
        )}
        {ranking && (
          <div className="absolute top-3 right-3 flex items-center gap-1 bg-white/90 backdrop-blur-sm px-2 py-1 rounded-full text-xs font-semibold text-amber-600">
            <Trophy size={11} />#{ranking}
          </div>
        )}
      </div>

      <div className="p-4 flex flex-col flex-1 gap-3">
        <div>
          <h3 className="font-semibold text-gray-900 leading-snug group-hover:text-primary-700 transition-colors line-clamp-2">
            {name}
          </h3>
          <div className="flex items-center gap-1 mt-1 text-sm text-gray-500">
            <MapPin size={13} />
            <span>
              {city}, {country}
            </span>
          </div>
        </div>

        <div className="flex flex-wrap gap-1">
          {specialties.slice(0, 3).map((s) => (
            <SpecialtyBadge key={s.id} name={s.name} />
          ))}
          {specialties.length > 3 && (
            <span className="text-xs text-gray-400">+{specialties.length - 3}</span>
          )}
        </div>

        <div className="mt-auto pt-3 border-t border-gray-50 flex items-center justify-between text-sm text-gray-500">
          {tuition && (
            <div className="flex items-center gap-1 font-medium text-gray-700">
              <DollarSign size={13} className="text-green-500" />
              {tuition}
            </div>
          )}
          {students_count && (
            <div className="flex items-center gap-1">
              <Users size={13} />
              {students_count.toLocaleString()} студентов
            </div>
          )}
        </div>
      </div>
    </Link>
  );
}
