import api from "./client";

export interface SummaryKPIs {
  total_income: number;
  total_expenses: number;
  net_savings: number;
  savings_rate: number;
  average_transaction_amount: number;
  transaction_count: number;
}

export interface CategoryBreakdownItem {
  category: string;
  total_amount: number;
  percentage: number;
  transaction_count: number;
}

export interface MonthlyTrendItem {
  month: string;
  income: number;
  expenses: number;
  net_savings: number;
}

export interface TopMerchantItem {
  merchant: string;
  total_amount: number;
  transaction_count: number;
}

export async function getSummary(): Promise<SummaryKPIs> {
  const response = await api.get("/analytics/summary");
  return response.data;
}

export async function getCategoryBreakdown(): Promise<CategoryBreakdownItem[]> {
  const response = await api.get("/analytics/category-breakdown");
  return response.data;
}

export async function getMonthlyTrend(): Promise<MonthlyTrendItem[]> {
  const response = await api.get("/analytics/monthly-trend");
  return response.data;
}

export async function getTopMerchants(): Promise<TopMerchantItem[]> {
  const response = await api.get("/analytics/top-merchants");
  return response.data;
}