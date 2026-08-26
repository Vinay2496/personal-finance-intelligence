import api from "./client";

export interface AskResponse {
  answer: string;
}

export async function askAiAnalyst(question: string): Promise<AskResponse> {
  const response = await api.post("/ai-analyst/ask", { question });
  return response.data;
}