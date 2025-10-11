import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import { ChevronDown } from "lucide-react";

type Category = {
  identifier: string;
  name: string;
};

type TodoCategoryListProps = {
  categories: Category[];
  selectedCategory: Category;
  onSelectCategory: (categoryDetail: Category) => void;
};

export default function TodoCategoryList({
  categories,
  selectedCategory,
  //
  onSelectCategory,
}: TodoCategoryListProps) {
  return (
    <Popover>
      <div className="flex gap-3 items-center">
        <PopoverTrigger asChild>
          <Button size="sm" variant="outline" className="w-max">
            {selectedCategory?.name}
            <ChevronDown />
          </Button>
        </PopoverTrigger>
      </div>

      <PopoverContent className="w-36 p-2">
        <div className="grid gap-2 max-h-64 overflow-auto">
          {categories.map((category) => (
            <div
              key={category.identifier}
              onClick={() => onSelectCategory(category)}
              className="p-2 cursor-pointer hover:bg-gray-100 transition-colors rounded-md"
            >
              <p className="text-sm text-gray-700">{category.name}</p>
            </div>
          ))}
        </div>
      </PopoverContent>
    </Popover>
  );
}
