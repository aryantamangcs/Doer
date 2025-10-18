import JournalListItem from "./journal-list-item";

import { Journal } from "./types";

type JournalListProps = {
  journals: Journal[];
};

export default function JournalList({ journals }: JournalListProps) {
  return (
    <div className="flex flex-col gap-3">
      {journals.map((journal) => (
        <JournalListItem key={journal.identifier} journal={journal} />
      ))}
    </div>
  );
}
