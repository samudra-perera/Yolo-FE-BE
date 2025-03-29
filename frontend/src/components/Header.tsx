import { Separator } from "@/components/ui/separator";

const Header = () => {
  return (
    <div className="w-full text-center py-6">
      <h1 className="text-4xl font-bold">TimsCup Detector</h1>
      <p className="text-muted-foreground text-lg mt-2">
        Identify Tim Hortons cups and generic coffee cups using AI
      </p>
      <Separator className="mt-4" />
    </div>
  );
};

export default Header;
