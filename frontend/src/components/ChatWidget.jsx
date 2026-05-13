import { useState, useRef, useEffect } from "react";
import { Link } from "react-router-dom";
import { MessageCircle, X, Send, Bot, User, MapPin, Trophy } from "lucide-react";
import { api } from "../api";

function TypingIndicator() {
  return (
    <div className="flex gap-2 items-end">
      <div className="w-7 h-7 rounded-full bg-primary-100 flex items-center justify-center flex-shrink-0">
        <Bot size={14} className="text-primary-600" />
      </div>
      <div className="bg-white border border-gray-100 rounded-2xl rounded-bl-sm px-4 py-3">
        <div className="flex gap-1 items-center">
          <span className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce [animation-delay:0ms]" />
          <span className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce [animation-delay:150ms]" />
          <span className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce [animation-delay:300ms]" />
        </div>
      </div>
    </div>
  );
}

function UniMiniCard({ university }) {
  return (
    <Link
      to={`/university/${university.id}`}
      className="flex items-center gap-3 p-3 bg-gray-50 hover:bg-primary-50 border border-gray-100 hover:border-primary-100 rounded-xl transition-colors"
    >
      <div className="w-10 h-10 rounded-lg overflow-hidden bg-gray-200 flex-shrink-0">
        {university.image_url ? (
          <img src={university.image_url} alt={university.name} className="w-full h-full object-cover" />
        ) : (
          <div className="w-full h-full bg-primary-100 flex items-center justify-center text-primary-500 font-bold text-sm">
            {university.name[0]}
          </div>
        )}
      </div>
      <div className="min-w-0 flex-1">
        <p className="text-sm font-medium text-gray-900 truncate">{university.name}</p>
        <div className="flex items-center gap-2 text-xs text-gray-500">
          <span className="flex items-center gap-0.5">
            <MapPin size={10} />{university.city}
          </span>
          {university.ranking && (
            <span className="flex items-center gap-0.5 text-amber-500">
              <Trophy size={10} />#{university.ranking}
            </span>
          )}
        </div>
      </div>
    </Link>
  );
}

function MessageBubble({ msg }) {
  const isUser = msg.role === "user";

  const renderText = (text) => {
    const parts = text.split(/(\*\*[^*]+\*\*)/g);
    return parts.map((part, i) =>
      part.startsWith("**") ? (
        <strong key={i}>{part.slice(2, -2)}</strong>
      ) : (
        part
      )
    );
  };

  return (
    <div className={`flex gap-2 items-end ${isUser ? "flex-row-reverse" : ""}`}>
      <div
        className={`w-7 h-7 rounded-full flex items-center justify-center flex-shrink-0 ${
          isUser ? "bg-primary-600" : "bg-primary-100"
        }`}
      >
        {isUser ? (
          <User size={14} className="text-white" />
        ) : (
          <Bot size={14} className="text-primary-600" />
        )}
      </div>
      <div className={`max-w-[80%] ${isUser ? "items-end" : "items-start"} flex flex-col gap-2`}>
        <div
          className={`px-4 py-3 rounded-2xl text-sm leading-relaxed whitespace-pre-line ${
            isUser
              ? "bg-primary-600 text-white rounded-br-sm"
              : "bg-white border border-gray-100 text-gray-800 rounded-bl-sm"
          }`}
        >
          {msg.content.split("\n").map((line, i) => (
            <span key={i}>
              {renderText(line)}
              {i < msg.content.split("\n").length - 1 && <br />}
            </span>
          ))}
        </div>
        {msg.universities && msg.universities.length > 0 && (
          <div className="w-full flex flex-col gap-2 mt-1">
            {msg.universities.map((u) => (
              <UniMiniCard key={u.id} university={u} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

const SUGGESTIONS = [
  "Computer Science в США",
  "Медицина в Европе",
  "Бесплатное обучение",
  "Топ-10 рейтинга",
];

export default function ChatWidget() {
  const [open, setOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef(null);
  const inputRef = useRef(null);

  useEffect(() => {
    if (open && messages.length === 0) {
      sendMessage("Привет!");
    }
  }, [open]);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  useEffect(() => {
    if (open) inputRef.current?.focus();
  }, [open]);

  async function sendMessage(text) {
    if (!text.trim() || loading) return;

    const userMsg = { role: "user", content: text.trim() };
    const next = [...messages, userMsg];
    setMessages(next);
    setInput("");
    setLoading(true);

    try {
      const data = await api.chat(next.map(({ role, content }) => ({ role, content })));
      setMessages([
        ...next,
        { role: "assistant", content: data.message, universities: data.universities },
      ]);
    } catch {
      setMessages([
        ...next,
        { role: "assistant", content: "Ошибка соединения. Попробуйте ещё раз." },
      ]);
    } finally {
      setLoading(false);
    }
  }

  function handleSubmit(e) {
    e.preventDefault();
    sendMessage(input);
  }

  return (
    <>
      <button
        onClick={() => setOpen((v) => !v)}
        className="fixed bottom-6 right-6 z-50 w-14 h-14 bg-primary-600 hover:bg-primary-700 text-white rounded-full shadow-lg flex items-center justify-center transition-all duration-200 hover:scale-105 active:scale-95"
        aria-label="Открыть чат"
      >
        {open ? <X size={22} /> : <MessageCircle size={22} />}
        {!open && messages.length === 0 && (
          <span className="absolute -top-1 -right-1 w-4 h-4 bg-green-400 rounded-full border-2 border-white" />
        )}
      </button>

      {open && (
        <div className="fixed bottom-24 right-6 z-50 w-[360px] max-w-[calc(100vw-2rem)] bg-white rounded-2xl shadow-2xl border border-gray-100 flex flex-col overflow-hidden"
          style={{ height: "520px" }}
        >
          <div className="px-4 py-3 bg-primary-600 flex items-center gap-3">
            <div className="w-8 h-8 rounded-full bg-white/20 flex items-center justify-center">
              <Bot size={18} className="text-white" />
            </div>
            <div>
              <p className="text-sm font-semibold text-white">AI Советник</p>
              <p className="text-xs text-primary-200">Подберу университет для вас</p>
            </div>
            <button
              onClick={() => setOpen(false)}
              className="ml-auto text-white/70 hover:text-white transition-colors"
            >
              <X size={18} />
            </button>
          </div>

          <div className="flex-1 overflow-y-auto chat-scroll p-4 flex flex-col gap-4 bg-gray-50">
            {messages.map((msg, i) => (
              <MessageBubble key={i} msg={msg} />
            ))}
            {loading && <TypingIndicator />}
            <div ref={bottomRef} />
          </div>

          {messages.length <= 1 && !loading && (
            <div className="px-4 pb-2 flex flex-wrap gap-2 bg-gray-50">
              {SUGGESTIONS.map((s) => (
                <button
                  key={s}
                  onClick={() => sendMessage(s)}
                  className="text-xs px-3 py-1.5 bg-white border border-gray-200 text-gray-600 hover:border-primary-300 hover:text-primary-700 rounded-full transition-colors"
                >
                  {s}
                </button>
              ))}
            </div>
          )}

          <form
            onSubmit={handleSubmit}
            className="p-3 border-t border-gray-100 bg-white flex gap-2"
          >
            <input
              ref={inputRef}
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Напишите сообщение..."
              disabled={loading}
              className="flex-1 px-4 py-2 text-sm bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent placeholder-gray-400 disabled:opacity-60"
            />
            <button
              type="submit"
              disabled={!input.trim() || loading}
              className="w-10 h-10 flex items-center justify-center bg-primary-600 hover:bg-primary-700 disabled:bg-gray-200 text-white rounded-xl transition-colors"
            >
              <Send size={16} />
            </button>
          </form>
        </div>
      )}
    </>
  );
}
