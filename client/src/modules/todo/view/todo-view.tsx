"use client";

import { useBoolean } from "minimal-shared";

import { Plus } from "lucide-react";

import { Button } from "@/components/ui/button";

import { Container } from "@/components/common";

import TodoCategoryList from "../todo-category-list";
import TodoCategoryCreateDialog from "../todo-category-create-dialog";

export default function TodoView() {
  const openCategoryCreate = useBoolean();

  return (
    <>
      <Container>
        <div className="flex flex-col gap-3">
          <div className="flex justify-between">
            <h1> Todo </h1>

            <Button size="sm" onClick={openCategoryCreate.onTrue}>
              <Plus />
              Add
            </Button>
          </div>

          <TodoCategoryList />
        </div>
      </Container>

      <TodoCategoryCreateDialog
        open={openCategoryCreate.value}
        onClose={openCategoryCreate.onFalse}
      />
    </>
  );
}
