import { Plus, ChevronDown } from "lucide-react";

import { Button } from "@/components/ui/button";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import { Separator } from "@/components/ui/separator";

type Category = {
  identifier: string;
  name: string;
};

type TodoCategoryListProps = {
  categories: Category[];
  selectedCategory: Category;
  onOpenCategoryDialog: () => void;
  onSelectCategory: (categoryDetail: Category) => void;
};

export default function TodoCategoryList({
  categories,
  selectedCategory,
  //
  onOpenCategoryDialog,
  onSelectCategory,
}: TodoCategoryListProps) {
  return (
    <Popover>
      <PopoverTrigger asChild>
        <Button size="sm" variant="outline" className="w-max">
          {selectedCategory?.name ?? "Category"}
          <ChevronDown />
        </Button>
      </PopoverTrigger>

      <PopoverContent align="start" className="w-38 p-2">
        <div className="grid gap-1 max-h-64 overflow-auto">
          <Button
            size="sm"
            variant="ghost"
            className="h-6 text-xs"
            onClick={onOpenCategoryDialog}
          >
            <Plus />
            Add Category
          </Button>

          {!!categories.length && <Separator />}

          {categories.map((category) => (
            <div
              key={category.identifier}
              onClick={() => onSelectCategory(category)}
              className="p-1 cursor-pointer hover:bg-gray-100 transition-colors rounded-md"
            >
              <p className="text-sm text-gray-700">{category.name}</p>
            </div>
          ))}
        </div>
      </PopoverContent>
    </Popover>
  );
}
