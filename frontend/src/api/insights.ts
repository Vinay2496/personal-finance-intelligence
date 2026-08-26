import api from "./client";

export interface MonthComparison {
  current_month: string;
  previous_month: string | null;
  current_expenses: number;
  previous_expenses: number | null;
  change_amount: number | null;
  change_percent: number | null;
}

export interface CategoryChange {
  category: string;
  current_amount: number;
  previous_amount: number;
  change_amount: number;
}

export interface RecurringExpense {
  merchant: string;
  average_amount: number;
  occurrence_count: number;
  frequency: string;
}

export interface UnusualTransaction {
  id: number;
  description: string;
  merchant: string | null;
  amount: number;
  transaction_date: string;
  reason: string;
}

export interface Insight {
  type: string;
  message: string;
}

export interface InsightsResponse {
  insights: Insight[];
  month_comparison: MonthComparison | null;
  category_changes: CategoryChange[];
  recurring_expenses: RecurringExpense[];
  unusual_transactions: UnusualTransaction[];
}

export async function getInsights(): Promise<InsightsResponse> {
  const response = await api.get("/insights");
  return response.data;
}