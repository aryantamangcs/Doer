import { useMemo } from "react";

import useSWR, { mutate } from "swr";

import { endpoints } from "./endpoints";

import { fetcher, poster, patcher, deleter } from "@/lib/api/http";

import { Category } from "@/modules/todo/types";

export function useGetCategories() {
  const { data, isLoading, error, isValidating } = useSWR(
    endpoints.todo.category,
    fetcher
  );

  const memoizedValue = useMemo(() => {
    return {
      categories: data?.data || [],
      categoriesLoading: isLoading,
      categoriesError: error,
    };
  }, [data, error, isLoading, isValidating]);

  return memoizedValue;
}

export const createCategory = async (categoryData: any) => {
  try {
    const response = await poster([endpoints.todo.category, categoryData]);

    mutate(endpoints.todo.category);

    return response.data;
  } catch (error) {
    throw error;
  }
};

export const deleteCategory = async (categoryData: any) => {
  try {
    const response = await poster([endpoints.todo.category, categoryData]);

    return response.data;
  } catch (error) {
    throw error;
  }
};

export const createTodo = async (todoData: any) => {
  try {
    const response = await poster([endpoints.todo.todo, todoData]);

    mutate(
      `${endpoints.todo.todo}?todo_list_identifier=${todoData.todo_list_identifier}`
    );

    return response.data;
  } catch (error) {
    throw error;
  }
};

export function useGetTodos(selectedCategory: Category) {
  const { data, isLoading, error, isValidating } = useSWR(
    `${endpoints.todo.todo}?todo_list_identifier=${selectedCategory?.identifier}`,
    fetcher
  );

  const memoizedValue = useMemo(() => {
    return {
      todos: data?.data || [],
      todosLoading: isLoading,
      todosError: error,
    };
  }, [data, error, isLoading, isValidating]);

  return memoizedValue;
}

export const updateTodo = async (todoData: any) => {
  try {
    const response = await patcher([
      `${endpoints.todo.todo}?todo_item_identifier=${todoData.identifier}`,
      todoData,
    ]);

    return response.data;
  } catch (error) {
    throw error;
  }
};

export const deleteTodo = async (identifier: string) => {
  try {
    const response = await deleter([
      `${endpoints.todo.todo}?identifier=${identifier}`,
    ]);

    return response.data;
  } catch (error) {
    throw error;
  }
};
