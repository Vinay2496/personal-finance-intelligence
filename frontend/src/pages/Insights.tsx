import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { getInsights } from "../api/insights";
import type { InsightsResponse } from "../api/insights";

export default function Insights() {
  const [data, setData] = useState<InsightsResponse | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getInsights()
      .then(setData)
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p className="text-gray-500">Loading insights...</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-2xl font-bold text-gray-800">Financial Insights</h1>
        <Link to="/dashboard" className="text-sm text-blue-600 hover:underline">
          Back to Dashboard
        </Link>
      </div>

      {/* Insight messages */}
      <div className="space-y-3 mb-8">
        {data?.insights.length === 0 && (
          <p className="text-gray-500">
            Not enough data yet to generate insights. Upload more transactions.
          </p>
        )}
        {data?.insights.map((insight, idx) => (
          <div
            key={idx}
            className="bg-white rounded-lg shadow p-4 border-l-4 border-blue-500"
          >
            <p className="text-gray-800">{insight.message}</p>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recurring Expenses */}
        <div className="bg-white rounded-lg shadow p-4">
          <h2 className="text-lg font-semibold text-gray-800 mb-4">
            Recurring Expenses
          </h2>
          {data?.recurring_expenses.length === 0 ? (
            <p className="text-gray-500 text-sm">No recurring expenses detected yet.</p>
          ) : (
            <ul className="divide-y">
              {data?.recurring_expenses.map((r, idx) => (
                <li key={idx} className="py-2 flex justify-between">
                  <span className="text-gray-700">{r.merchant}</span>
                  <span className="text-gray-900 font-medium">
                    ₹{r.average_amount.toLocaleString()}/mo
                  </span>
                </li>
              ))}
            </ul>
          )}
        </div>

        {/* Unusual Transactions */}
        <div className="bg-white rounded-lg shadow p-4">
          <h2 className="text-lg font-semibold text-gray-800 mb-4">
            Unusual Transactions
          </h2>
          {data?.unusual_transactions.length === 0 ? (
            <p className="text-gray-500 text-sm">No unusual transactions detected.</p>
          ) : (
            <ul className="divide-y">
              {data?.unusual_transactions.map((t) => (
                <li key={t.id} className="py-2">
                  <div className="flex justify-between">
                    <span className="text-gray-700">{t.description}</span>
                    <span className="text-red-600 font-medium">
                      ₹{t.amount.toLocaleString()}
                    </span>
                  </div>
                  <p className="text-xs text-gray-500 mt-1">{t.reason}</p>
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
    </div>
  );
}