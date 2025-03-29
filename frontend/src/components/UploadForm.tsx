import { useState } from "react";
import { Button } from "@/components/ui/button";

interface UploadFormProps {
  selectedModel: string;
  onResult: (result: any, file: File) => void;
}

export const UploadForm = ({ selectedModel, onResult }: UploadFormProps) => {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) return;

    const formData = new FormData();
    formData.append("image", file);
    formData.append("model", selectedModel);

    setLoading(true);
    try {
      const response = await fetch("http://localhost:8000/predict", {
        method: "POST",
        body: formData,
      });
      const data = await response.json();
      onResult(data, file); // ✅ Pass both data and file
    } catch (err) {
      console.error("Prediction failed", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="max-w-md mx-auto mt-6 p-4 border rounded-xl shadow-sm"
    >
      <label className="block mb-2 text-sm font-medium">Upload an Image</label>
      <input
        type="file"
        accept="image/*"
        onChange={(e) => setFile(e.target.files?.[0] || null)}
        className="mb-4"
      />
      <Button type="submit" disabled={loading || !file}>
        {loading ? "Predicting..." : "Run Prediction"}
      </Button>
    </form>
  );
};
