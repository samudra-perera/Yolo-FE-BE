import { useEffect, useState } from "react";

interface ModelInfoProps {
  model: string;
}

export const ModelInfo = ({ model }: ModelInfoProps) => {
  const [info, setInfo] = useState<null | {
    config: {
      input_size: number[];
      batch_size: number;
      confidence_threshold: number;
      [key: string]: any;
    };
    date_registered: string;
  }>(null);

  useEffect(() => {
    if (!model) return;

    fetch(`http://localhost:8000/management/models/${model}/describe`)
      .then((res) => res.json())
      .then((data) => setInfo(data))
      .catch((err) => console.error("Failed to fetch model info:", err));
  }, [model]);

  if (!info) return null;

  return (
    <div className="max-w-md mx-auto mt-6 p-6 rounded-xl bg-muted shadow">
      <h3 className="text-lg font-semibold mb-2">Model Information</h3>
      <ul className="text-sm space-y-1">
        <li>
          <strong>Input Size:</strong> {info.config.input_size.join(" x ")}
        </li>
        <li>
          <strong>Batch Size:</strong> {info.config.batch_size}
        </li>
        <li>
          <strong>Confidence Threshold:</strong>{" "}
          {info.config.confidence_threshold}
        </li>
        <li>
          <strong>Date Registered:</strong> {info.date_registered}
        </li>
      </ul>
    </div>
  );
};
