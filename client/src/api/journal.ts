import { useMemo } from "react";

import useSWR, { mutate } from "swr";

import { endpoints } from "./endpoints";

import { fetcher, poster } from "@/lib/api/http";

export const createJournal = async (journalData: any) => {
  try {
    const response = await poster([endpoints.journal, journalData]);

    mutate(endpoints.journal);

    return response.data;
  } catch (error) {
    throw error;
  }
};

export function useGetJournals() {
  const { data, isLoading, error, isValidating } = useSWR(
    endpoints.journal,
    fetcher
  );

  const memoizedValue = useMemo(() => {
    return {
      journals: data?.data || [],
      journalsLoading: isLoading,
      journalsError: error,
    };
  }, [data, error, isLoading, isValidating]);

  return memoizedValue;
}
