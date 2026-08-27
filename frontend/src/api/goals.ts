import api from "./client";

export interface Goal {
  id: number;
  name: string;
  target_amount: number;
  deadline: string;
  current_savings: number;
  required_monthly_saving: number;
  months_remaining: number;
  on_track: boolean;
}

export interface GoalCreate {
  name: string;
  target_amount: number;
  deadline: string;
}

export async function getGoals(): Promise<Goal[]> {
  const response = await api.get("/goals");
  return response.data;
}

export async function createGoal(goal: GoalCreate): Promise<Goal> {
  const response = await api.post("/goals", goal);
  return response.data;
}

export async function deleteGoal(id: number): Promise<void> {
  await api.delete(`/goals/${id}`);
}