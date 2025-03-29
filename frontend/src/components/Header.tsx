import { Card, CardContent } from "@/components/ui/card";

const Header = () => {
  return (
    <Card className="mt-6 mx-auto max-w-3xl shadow-lg rounded-2xl p-6 text-center bg-white dark:bg-zinc-900">
      <CardContent>
        <h1 className="text-3xl font-bold mb-2 tracking-tight">
          🧠 Smart Cup Detector
        </h1>
        <p className="text-muted-foreground text-sm">
          Detect Tim Hortons cups and generic coffee cups using YOLOv8.
        </p>
      </CardContent>
    </Card>
  );
};

export default Header;
