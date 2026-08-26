import { useState, useRef, useEffect } from "react";
import { Link } from "react-router-dom";
import { askAiAnalyst } from "../api/aiAnalyst";

interface ChatMessage {
  role: "user" | "assistant";
  content: string;
}

export default function AiAnalyst() {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      role: "assistant",
      content:
        "Hi! Ask me anything about your spending — e.g. \"What did I spend the most on last month?\" or \"Am I overspending on food?\"",
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  async function handleSend() {
    const question = input.trim();
    if (!question || loading) return;

    setMessages((prev) => [...prev, { role: "user", content: question }]);
    setInput("");
    setLoading(true);

    try {
      const res = await askAiAnalyst(question);
      setMessages((prev) => [...prev, { role: "assistant", content: res.answer }]);
    } catch {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "Sorry, something went wrong answering that. Please try again.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  function handleKeyDown(e: React.KeyboardEvent<HTMLInputElement>) {
    if (e.key === "Enter") {
      handleSend();
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 p-8 flex flex-col">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-gray-800">AI Financial Analyst</h1>
        <Link to="/dashboard" className="text-sm text-blue-600 hover:underline">
          Back to Dashboard
        </Link>
      </div>

      <div className="flex-1 bg-white rounded-lg shadow p-4 flex flex-col max-w-3xl w-full mx-auto">
        <div className="flex-1 overflow-y-auto space-y-4 mb-4" style={{ maxHeight: "60vh" }}>
          {messages.map((msg, i) => (
            <div
              key={i}
              className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
            >
              <div
                className={`max-w-[80%] rounded-lg px-4 py-2 whitespace-pre-wrap ${
                  msg.role === "user"
                    ? "bg-blue-600 text-white"
                    : "bg-gray-100 text-gray-800"
                }`}
              >
                {msg.content}
              </div>
            </div>
          ))}
          {loading && (
            <div className="flex justify-start">
              <div className="bg-gray-100 text-gray-500 rounded-lg px-4 py-2">
                Thinking...
              </div>
            </div>
          )}
          <div ref={bottomRef} />
        </div>

        <div className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask about your spending..."
            className="flex-1 border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            disabled={loading}
          />
          <button
            onClick={handleSend}
            disabled={loading || !input.trim()}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50"
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
}