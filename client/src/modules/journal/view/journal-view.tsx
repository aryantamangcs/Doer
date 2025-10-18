"use client";

import { Plus } from "lucide-react";
import { useBoolean } from "minimal-shared";

import { Container } from "@/components/common";

import { Button } from "@/components/ui/button";

import { useGetJournals } from "@/api/journal";

import JournalList from "../journal-list";
import JournalDialog from "../journal-dialog";

export default function JournalView() {
  const openJournalDialog = useBoolean();

  const { journals } = useGetJournals();

  return (
    <>
      <Container>
        <div className="flex flex-col gap-4">
          <div className="flex items-center justify-between">
            <h1 className="text-xl font-bold">Journal</h1>

            <Button size="sm" onClick={openJournalDialog.onTrue}>
              <Plus />
              Add Journal
            </Button>
          </div>

          <JournalList journals={journals} />
        </div>
      </Container>

      <JournalDialog
        open={openJournalDialog.value}
        onClose={openJournalDialog.onFalse}
      />
    </>
  );
}
