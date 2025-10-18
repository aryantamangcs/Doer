import { Card } from "@/components/ui/card";

import { Journal } from "./types";

type JournalListProps = {
  journal: Journal;
};

export default function JournalListItem({ journal }: JournalListProps) {
  const { identifier, title, content } = journal || {};

  return (
    <Card className="p-2">
      <h6 className="font-bold"> {title} </h6>

      <p className="text-muted-foreground"> {content} </p>
    </Card>
  );
}
