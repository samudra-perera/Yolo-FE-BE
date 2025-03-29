import { useState } from "react";
import Header from "./components/Header.tsx";
import { GroupInfo } from "./components/GroupInfo.tsx";
import { ModelSelector } from "./components/ModelSelector.tsx";
import { ModelInfo } from "./components/ModelInfo.tsx";
import { UploadForm } from "./components/UploadForm.tsx";
import { PredictionDisplay } from "./components/PredictionDisplay.tsx";

function App() {
  const [selectedModel, setSelectedModel] = useState("");
  const [result, setResult] = useState<any>(null);
  const [imageURL, setImageURL] = useState("");

  const handleResult = (data: any, file: File) => {
    setResult(data);
    setImageURL(URL.createObjectURL(file));
  };

  return (
    <div className="min-h-screen bg-background text-foreground px-4">
      <Header />
      <ModelSelector
        selectedModel={selectedModel}
        onChange={setSelectedModel}
      />
      <ModelInfo model={selectedModel} />
      <GroupInfo />
      <UploadForm selectedModel={selectedModel} onResult={handleResult} />
      {result && imageURL && (
        <PredictionDisplay
          imageUrl={imageURL}
          predictions={result.predictions}
        />
      )}
    </div>
  );
}

export default App;
