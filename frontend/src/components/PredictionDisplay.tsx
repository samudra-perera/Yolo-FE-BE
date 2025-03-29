import { useEffect, useRef } from "react";

interface Prediction {
  label: string;
  confidence: number;
  bbox: [number, number, number, number]; // [x1, y1, x2, y2]
}

interface Props {
  imageUrl: string;
  predictions: Prediction[];
}

export const PredictionDisplay = ({ imageUrl, predictions }: Props) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const imageRef = useRef<HTMLImageElement>(null);

  useEffect(() => {
    const draw = () => {
      const canvas = canvasRef.current;
      const img = imageRef.current;
      if (!canvas || !img) return;

      const ctx = canvas.getContext("2d");
      if (!ctx) return;

      canvas.width = img.width;
      canvas.height = img.height;
      ctx.drawImage(img, 0, 0);

      predictions.forEach(({ label, confidence, bbox }) => {
        const [x1, y1, x2, y2] = bbox;

        ctx.strokeStyle = "#ff5252";
        ctx.lineWidth = 2;
        ctx.strokeRect(x1, y1, x2 - x1, y2 - y1);

        ctx.fillStyle = "#ff5252";
        ctx.font = "16px sans-serif";
        ctx.fillText(
          `${label} (${confidence}%)`,
          x1,
          y1 > 20 ? y1 - 5 : y1 + 15,
        );
      });
    };

    const img = imageRef.current;
    if (img?.complete) draw();
    else img!.onload = draw;
  }, [imageUrl, predictions]);

  return (
    <div className="max-w-3xl mx-auto mt-8 relative">
      <img ref={imageRef} src={imageUrl} alt="Uploaded" className="w-full" />
      <canvas
        ref={canvasRef}
        className="absolute top-0 left-0 w-full h-full pointer-events-none"
      />
    </div>
  );
};
