import { useEffect, useState } from "react";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

interface ModelSelectorProps {
  selectedModel: string;
  onChange: (model: string) => void;
}

export const ModelSelector = ({
  selectedModel,
  onChange,
}: ModelSelectorProps) => {
  const [models, setModels] = useState<string[]>([]);

  useEffect(() => {
    fetch("http://localhost:8000/management/models")
      .then((res) => res.json())
      .then((data) => setModels(data.available_models))
      .catch((err) => console.error("Failed to fetch models:", err));
  }, []);

  useEffect(() => {
    if (!selectedModel) return;

    fetch(
      `http://localhost:8000/management/models/${selectedModel}/set-default`,
    )
      .then((res) => res.json())
      .then((data) => {
        if (!data.success) {
          console.warn("Failed to set default model:", data);
        }
      })
      .catch((err) => console.error("Error setting default model:", err));
  }, [selectedModel]);

  return (
    <div className="max-w-md mx-auto mt-6">
      <label className="block mb-2 text-sm font-medium">Select Model</label>
      <Select value={selectedModel} onValueChange={onChange}>
        <SelectTrigger>
          <SelectValue placeholder="Choose a model..." />
        </SelectTrigger>
        <SelectContent>
          {models.map((model) => (
            <SelectItem key={model} value={model}>
              {model}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
    </div>
  );
};
