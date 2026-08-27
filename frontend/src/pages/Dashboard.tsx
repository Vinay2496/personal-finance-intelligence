import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import {
  getSummary,
  getCategoryBreakdown,
  getMonthlyTrend,
  getTopMerchants,
} from "../api/analytics";
import type {
  SummaryKPIs,
  CategoryBreakdownItem,
  MonthlyTrendItem,
  TopMerchantItem,
} from "../api/analytics";
import { getForecast } from "../api/forecast";
import type { ForecastResult } from "../api/forecast";
import {
  BarChart,
  Bar,
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  ResponsiveContainer,
  CartesianGrid,
} from "recharts";

const COLORS = [
  "#3b82f6",
  "#f97316",
  "#10b981",
  "#8b5cf6",
  "#ef4444",
  "#eab308",
  "#06b6d4",
  "#ec4899",
];

export default function Dashboard() {
  const { user, logout } = useAuth();
  const [summary, setSummary] = useState<SummaryKPIs | null>(null);
  const [categories, setCategories] = useState<CategoryBreakdownItem[]>([]);
  const [trend, setTrend] = useState<MonthlyTrendItem[]>([]);
  const [merchants, setMerchants] = useState<TopMerchantItem[]>([]);
  const [forecast, setForecast] = useState<ForecastResult | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      try {
        const [summaryData, categoryData, trendData, merchantData, forecastData] =
          await Promise.all([
            getSummary(),
            getCategoryBreakdown(),
            getMonthlyTrend(),
            getTopMerchants(),
            getForecast(),
          ]);
        setSummary(summaryData);
        setCategories(categoryData);
        setTrend(trendData);
        setMerchants(merchantData);
        setForecast(forecastData);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p className="text-gray-500">Loading dashboard...</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-2xl font-bold text-gray-800">
          Welcome, {user?.name}
        </h1>
        <div className="flex items-center gap-4">
          <Link to="/insights" className="text-sm text-blue-600 hover:underline">
            View Insights
          </Link>
	  <Link to="/ai-analyst" className="text-sm text-blue-600 hover:underline">
            Ask AI Analyst
          </Link>
          <Link to="/goals" className="text-sm text-blue-600 hover:underline">
            Goals
          </Link>
          <button
            onClick={logout}
            className="text-sm text-red-600 hover:underline"
          >
            Log Out
          </button>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <KpiCard label="Income" value={`₹${summary?.total_income.toLocaleString()}`} />
        <KpiCard label="Expenses" value={`₹${summary?.total_expenses.toLocaleString()}`} />
        <KpiCard label="Savings" value={`₹${summary?.net_savings.toLocaleString()}`} />
        <KpiCard label="Savings Rate" value={`${summary?.savings_rate}%`} />
      </div>

      {/* Forecast Card */}
      <div className="bg-white rounded-lg shadow p-4 mb-8">
        <h2 className="text-lg font-semibold text-gray-800 mb-2">
          Next Month Forecast
        </h2>
        {forecast?.reliable ? (
          <div>
            <p className="text-2xl font-bold text-gray-800">
              ₹{forecast.predicted_expenses?.toLocaleString()}
            </p>
            <p className="text-sm text-gray-500 mt-1">
              Predicted expenses for {forecast.forecast_month} · method: {forecast.method_used}
            </p>
            <p className="text-xs text-gray-400 mt-1">
              Based on {forecast.historical_months_used} months of data
              {forecast.mae !== null ? ` · avg error ±₹${forecast.mae?.toLocaleString()}` : ""}
            </p>
          </div>
        ) : (
          <p className="text-sm text-gray-500">
            {forecast?.reliability_note ?? "Not enough data yet to generate a reliable forecast."}
          </p>
        )}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        {/* Monthly Trend */}
        <div className="bg-white rounded-lg shadow p-4">
          <h2 className="text-lg font-semibold text-gray-800 mb-4">
            Monthly Spending Trend
          </h2>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={trend}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="month" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="income" stroke="#10b981" name="Income" />
              <Line type="monotone" dataKey="expenses" stroke="#ef4444" name="Expenses" />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Category Breakdown */}
        <div className="bg-white rounded-lg shadow p-4">
          <h2 className="text-lg font-semibold text-gray-800 mb-4">
            Spending by Category
          </h2>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={categories}
                dataKey="total_amount"
                nameKey="category"
                cx="50%"
                cy="50%"
                outerRadius={100}
                               label={(entry: any) => entry.category}
              >
                {categories.map((_, index) => (
                  <Cell key={index} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Top Merchants */}
      <div className="bg-white rounded-lg shadow p-4">
        <h2 className="text-lg font-semibold text-gray-800 mb-4">
          Top Merchants
        </h2>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={merchants}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="merchant" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="total_amount" fill="#3b82f6" name="Total Spent" />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

function KpiCard({ label, value }: { label: string; value: string }) {
  return (
    <div className="bg-white rounded-lg shadow p-4">
      <p className="text-sm text-gray-500">{label}</p>
      <p className="text-2xl font-bold text-gray-800">{value}</p>
    </div>
  );
}