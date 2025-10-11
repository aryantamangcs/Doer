import { Card } from "@/components/ui/card";

const categories = [
  {
    id: 1,
    name: "Home",
  },
  {
    id: 1,
    name: "Study",
  },
];

export default function TodoCategoryList() {
  return (
    <div className="grid gap-3 grid-cols-8">
      {categories.map((category) => (
        <Card className="p-2">
          <p className="text-sm"> {category.name} </p>
        </Card>
      ))}
    </div>
  );
}
