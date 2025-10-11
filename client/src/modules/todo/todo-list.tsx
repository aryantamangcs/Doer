"use client";

import { useState, useEffect } from "react";
import { Plus, Trash2 } from "lucide-react";
import { toast } from "sonner";

import { Button } from "@/components/ui/button";
import { Checkbox } from "@/components/ui/checkbox";

import { useGetTodos, updateTodo, deleteTodo } from "@/api/todo";

import { Category, Todo } from "./types";

type TodoListProps = {
  selectedCategory: Category;
  onOpenTodoDialog: () => void;
};

export default function TodoList({
  selectedCategory,
  //
  onOpenTodoDialog,
}: TodoListProps) {
  const { todos } = useGetTodos(selectedCategory);

  const [todoList, setTodoList] = useState<Todo[]>([]);

  const handleComplete = async (identifier: string) => {
    try {
      const selectedTodo = todoList.find((t) => t.identifier === identifier);

      const status =
        selectedTodo?.status === "pending" ? "completed" : "pending";

      await updateTodo({ identifier, status });

      const updatedTodoList = todoList.map((t) =>
        t.identifier === identifier
          ? {
              ...t,
              status: t.status === "pending" ? "completed" : "pending",
            }
          : t
      );

      setTodoList(updatedTodoList);
    } catch (error) {
      toast.error("Couldn't complete todo!");
    }
  };

  const handleDelete = async (identifier: string) => {
    try {
      await deleteTodo(identifier);

      const updatedTodoList = todoList.filter(
        (t) => t.identifier != identifier
      );

      setTodoList(updatedTodoList);

      toast.success("Todo deleted successfully!");
    } catch (error) {
      toast.success("Couldn't delete todo!");
    }
  };

  useEffect(() => {
    setTodoList(todos);
  }, [todos]);

  return (
    <div className="">
      <div className="flex items-center justify-between">
        <h6 className="font-bold text-lg">Todo List</h6>

        <Button
          size="sm"
          onClick={onOpenTodoDialog}
          className="flex items-center gap-2"
        >
          <Plus className="h-4 w-4" /> Add Todo
        </Button>
      </div>

      <div className="divide-y divide-border">
        {todoList.length === 0 ? (
          <div className="p-12 text-center">
            <p className="text-muted-foreground text-lg">
              No tasks yet. Add one to get started!
            </p>
          </div>
        ) : (
          todoList.map((todo: Todo) => (
            <TodoItem
              key={todo.identifier}
              todo={todo}
              //
              onComplete={handleComplete}
              onDelete={handleDelete}
            />
          ))
        )}
      </div>

      {todoList.length > 0 && (
        <div className="p-4 bg-secondary/30 border-t border-border">
          <p className="text-sm text-muted-foreground text-center">
            {todoList.filter((t) => t.status !== "completed").length} of{" "}
            {todoList.length} tasks remaining
          </p>
        </div>
      )}
    </div>
  );
}

type TodoItemProps = {
  todo: Todo;
  onComplete: (id: string) => void;
  onDelete: (identifier: string) => void;
};

function TodoItem({
  todo,
  //
  onComplete,
  onDelete,
}: TodoItemProps) {
  const { identifier, title, status } = todo;

  const isCompleted = status === "completed";

  return (
    <div className="group p-5 hover:bg-secondary/50 transition-colors flex items-center gap-4">
      <Checkbox
        checked={isCompleted}
        onCheckedChange={() => onComplete(identifier)}
        className="h-5 w-5"
      />

      <label
        htmlFor={identifier}
        className={`flex-1 text-lg cursor-pointer select-none transition-all ${
          isCompleted ? "text-muted-foreground line-through" : "text-foreground"
        }`}
      >
        {title}
      </label>

      <Button
        variant="ghost"
        size="icon"
        onClick={() => onDelete(identifier)}
        className="opacity-0 group-hover:opacity-100 transition-opacity text-muted-foreground hover:text-destructive hover:bg-destructive/10"
      >
        <Trash2 className="h-4 w-4" />
      </Button>
    </div>
  );
}
