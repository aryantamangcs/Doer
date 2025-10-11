"use client";

import { useEffect, useState } from "react";

import { useBoolean } from "minimal-shared";

import { Plus } from "lucide-react";

import { Button } from "@/components/ui/button";

import { Container } from "@/components/common";

import { useGetCategories, useGetTodos } from "@/api/todo";

import { Category } from "../types";

import TodoCategoryList from "../todo-category-list";
import TodoList from "../todo-list";
import TodoCategoryCreateDialog from "../todo-category-create-dialog";
import TodoCreateDialog from "../todo-create-dialog";

export default function TodoView() {
  const openCategoryCreate = useBoolean();

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
          <div className="flex justify-between">
            <h1> Todo </h1>

            <Button size="sm" onClick={openCategoryCreate.onTrue}>
              <Plus />
              Add Category
            </Button>
          </div>

          <TodoCategoryList
            categories={categories}
            selectedCategory={selectedCategory}
            //
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
        open={openCategoryCreate.value}
        onClose={openCategoryCreate.onFalse}
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
