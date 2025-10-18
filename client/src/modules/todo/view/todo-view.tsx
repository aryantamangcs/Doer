"use client";

import { useEffect, useState } from "react";

import { useBoolean } from "minimal-shared";

import { Container } from "@/components/common";

import { useGetCategories } from "@/api/todo";

import { Category } from "../types";

import TodoCategoryList from "../todo-category-list";
import TodoList from "../todo-list";
import TodoCategoryCreateDialog from "../todo-category-create-dialog";
import TodoCreateDialog from "../todo-create-dialog";

export default function TodoView() {
  const openCategoryDialog = useBoolean();

  const openTodoDialog = useBoolean();

  const { categories } = useGetCategories();

  const [selectedCategory, setSelectedCategory] = useState<Category>(
    categories[0]
  );

  const handleSelectCategory = (categoryDetail: Category) => {
    setSelectedCategory(categoryDetail);
  };

  useEffect(() => {
    if (!categories.length) return;

    setSelectedCategory(categories[0]);
  }, [categories]);

  return (
    <>
      <Container>
        <div className="flex flex-col gap-3">
          <TodoCategoryList
            categories={categories}
            selectedCategory={selectedCategory}
            //
            onOpenCategoryDialog={openCategoryDialog.onTrue}
            onSelectCategory={handleSelectCategory}
          />

          <TodoList
            selectedCategory={selectedCategory}
            //
            onOpenTodoDialog={openTodoDialog.onTrue}
          />
        </div>
      </Container>

      <TodoCategoryCreateDialog
        open={openCategoryDialog.value}
        onClose={openCategoryDialog.onFalse}
      />

      <TodoCreateDialog
        open={openTodoDialog.value}
        onClose={openTodoDialog.onFalse}
        //
        selectedCategory={selectedCategory}
      />
    </>
  );
}
