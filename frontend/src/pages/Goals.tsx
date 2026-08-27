import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { getGoals, createGoal, deleteGoal } from "../api/goals";
import type { Goal } from "../api/goals";

export default function Goals() {
  const [goals, setGoals] = useState<Goal[]>([]);
  const [loading, setLoading] = useState(true);
  const [name, setName] = useState("");
  const [targetAmount, setTargetAmount] = useState("");
  const [deadline, setDeadline] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");

  async function loadGoals() {
    try {
      const data = await getGoals();
      setGoals(data);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadGoals();
  }, []);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");

    if (!name || !targetAmount || !deadline) {
      setError("Please fill in all fields.");
      return;
    }

    setSubmitting(true);
    try {
      await createGoal({
        name,
        target_amount: parseFloat(targetAmount),
        deadline,
      });
      setName("");
      setTargetAmount("");
      setDeadline("");
      await loadGoals();
    } catch {
      setError("Failed to create goal. Please try again.");
    } finally {
      setSubmitting(false);
    }
  }

  async function handleDelete(id: number) {
    await deleteGoal(id);
    await loadGoals();
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p className="text-gray-500">Loading goals...</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-2xl font-bold text-gray-800">Financial Goals</h1>
        <Link to="/dashboard" className="text-sm text-blue-600 hover:underline">
          Back to Dashboard
        </Link>
      </div>

      {/* New Goal Form */}
      <div className="bg-white rounded-lg shadow p-4 mb-8 max-w-2xl">
        <h2 className="text-lg font-semibold text-gray-800 mb-4">Add a New Goal</h2>
        <form onSubmit={handleSubmit} className="flex flex-col gap-3">
          <input
            type="text"
            placeholder="Goal name (e.g. Emergency Fund)"
            value={name}
            onChange={(e) => setName(e.target.value)}
            className="border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <input
            type="number"
            placeholder="Target amount (₹)"
            value={targetAmount}
            onChange={(e) => setTargetAmount(e.target.value)}
            className="border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <input
            type="date"
            value={deadline}
            onChange={(e) => setDeadline(e.target.value)}
            className="border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          {error && <p className="text-sm text-red-600">{error}</p>}
          <button
            type="submit"
            disabled={submitting}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50 w-fit"
          >
            {submitting ? "Adding..." : "Add Goal"}
          </button>
        </form>
      </div>

      {/* Goals List */}
      {goals.length === 0 ? (
        <p className="text-gray-500">No goals yet. Add one above to get started.</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 max-w-4xl">
          {goals.map((goal) => (
            <div key={goal.id} className="bg-white rounded-lg shadow p-4">
              <div className="flex justify-between items-start mb-2">
                <h3 className="text-lg font-semibold text-gray-800">{goal.name}</h3>
                <button
                  onClick={() => handleDelete(goal.id)}
                  className="text-sm text-red-600 hover:underline"
                >
                  Delete
                </button>
              </div>
              <p className="text-sm text-gray-500 mb-1">
                Target: ₹{goal.target_amount.toLocaleString()} by {goal.deadline}
              </p>
              <p className="text-sm text-gray-500 mb-1">
                Current savings: ₹{goal.current_savings.toLocaleString()}
              </p>
              <p className="text-sm text-gray-500 mb-3">
                {goal.months_remaining > 0
                  ? `Need ₹${goal.required_monthly_saving.toLocaleString()}/month for ${goal.months_remaining} month(s)`
                  : "Deadline reached"}
              </p>
              <span
                className={`inline-block text-xs font-semibold px-2 py-1 rounded ${
                  goal.on_track
                    ? "bg-green-100 text-green-700"
                    : "bg-red-100 text-red-700"
                }`}
              >
                {goal.on_track ? "On Track" : "Behind"}
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}