import { FC } from "react";
import { Card, CardContent } from "@/components/ui/card";

const Header: FC = () => {
  return (
    <Card className="mt-6 mx-auto max-w-3xl shadow-md rounded-2xl p-6 text-center">
      <CardContent>
        <h1 className="text-3xl font-bold">Cup Classifier</h1>
        <p className="text-muted-foreground mt-2 text-lg">
          Detects Tim Hortons cups and generic coffee cups using AI
        </p>
      </CardContent>
    </Card>
  );
};

export default Header;
