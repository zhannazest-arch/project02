import { ChevronLeft, ChevronRight } from "lucide-react";
import clsx from "clsx";

export default function Pagination({ page, pages, onChange }) {
  if (pages <= 1) return null;

  const items = [];
  for (let i = 1; i <= pages; i++) {
    if (i === 1 || i === pages || Math.abs(i - page) <= 1) {
      items.push(i);
    } else if (items[items.length - 1] !== "...") {
      items.push("...");
    }
  }

  return (
    <div className="flex items-center justify-center gap-1">
      <button
        onClick={() => onChange(page - 1)}
        disabled={page === 1}
        className="p-2 rounded-lg text-gray-500 hover:bg-gray-100 disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
      >
        <ChevronLeft size={16} />
      </button>

      {items.map((item, idx) =>
        item === "..." ? (
          <span key={`ellipsis-${idx}`} className="px-2 text-gray-400 text-sm">
            …
          </span>
        ) : (
          <button
            key={item}
            onClick={() => onChange(item)}
            className={clsx(
              "w-9 h-9 rounded-lg text-sm font-medium transition-colors",
              item === page
                ? "bg-primary-600 text-white"
                : "text-gray-600 hover:bg-gray-100"
            )}
          >
            {item}
          </button>
        )
      )}

      <button
        onClick={() => onChange(page + 1)}
        disabled={page === pages}
        className="p-2 rounded-lg text-gray-500 hover:bg-gray-100 disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
      >
        <ChevronRight size={16} />
      </button>
    </div>
  );
}
