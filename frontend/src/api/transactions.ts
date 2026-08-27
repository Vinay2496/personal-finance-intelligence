import api from "./client";

export interface UploadResult {
  total_rows: number;
  inserted: number;
  duplicates_skipped: number;
  invalid_rows: number;
  errors: string[];
}

export async function uploadTransactions(file: File): Promise<UploadResult> {
  const formData = new FormData();
  formData.append("file", file);

  const response = await api.post("/transactions/upload", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return response.data;
}