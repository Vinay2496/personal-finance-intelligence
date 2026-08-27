import { useState } from "react";
import { Link } from "react-router-dom";
import { uploadTransactions } from "../api/transactions";
import type { UploadResult } from "../api/transactions";

export default function Upload() {
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [result, setResult] = useState<UploadResult | null>(null);
  const [error, setError] = useState("");

  async function handleUpload() {
    if (!file) return;
    setUploading(true);
    setError("");
    setResult(null);

    try {
      const res = await uploadTransactions(file);
      setResult(res);
    } catch (err: any) {
      setError(
        err?.response?.data?.detail || "Upload failed. Please check your file and try again."
      );
    } finally {
      setUploading(false);
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-2xl font-bold text-gray-800">Upload Transactions</h1>
        <Link to="/dashboard" className="text-sm text-blue-600 hover:underline">
          Back to Dashboard
        </Link>
      </div>

      <div className="bg-white rounded-lg shadow p-6 max-w-2xl">
        <p className="text-sm text-gray-500 mb-4">
          Upload a CSV or Excel file with columns for date, description, amount, and type
          (debit/credit). Duplicate transactions are automatically skipped.
        </p>

        <input
          type="file"
          accept=".csv,.xlsx,.xls"
          onChange={(e) => setFile(e.target.files?.[0] || null)}
          className="mb-4 block w-full text-sm text-gray-600 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:bg-blue-50 file:text-blue-700 file:font-medium hover:file:bg-blue-100"
        />

        <button
          onClick={handleUpload}
          disabled={!file || uploading}
          className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50"
        >
          {uploading ? "Uploading..." : "Upload"}
        </button>

        {error && (
          <div className="mt-4 bg-red-50 text-red-700 text-sm rounded-lg p-3">{error}</div>
        )}

        {result && (
          <div className="mt-6 space-y-2">
            <p className="text-sm text-gray-800">
              <span className="font-semibold">{result.inserted}</span> transaction(s) imported
              successfully.
            </p>
            <p className="text-sm text-gray-500">
              {result.duplicates_skipped} duplicate(s) skipped, {result.invalid_rows} invalid
              row(s) skipped, out of {result.total_rows} total rows.
            </p>
            {result.errors.length > 0 && (
              <div className="mt-2 bg-yellow-50 rounded-lg p-3 text-xs text-yellow-800 max-h-40 overflow-y-auto">
                {result.errors.map((err, i) => (
                  <div key={i}>{err}</div>
                ))}
              </div>
            )}
            <Link
              to="/dashboard"
              className="inline-block mt-2 text-sm text-blue-600 hover:underline"
            >
              View Dashboard →
            </Link>
          </div>
        )}
      </div>
    </div>
  );
}