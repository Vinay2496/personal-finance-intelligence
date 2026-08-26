import api from "./client";

export interface ForecastResult {
  forecast_month: string | null;
  predicted_expenses: number | null;
  method_used: string | null;
  reliable: boolean;
  reliability_note: string;
  mae: number | null;
  historical_months_used: number;
}

export async function getForecast(): Promise<ForecastResult> {
  const response = await api.get("/forecast");
  return response.data;
}