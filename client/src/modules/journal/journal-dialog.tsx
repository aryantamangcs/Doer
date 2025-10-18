import { z } from "zod";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { toast } from "sonner";

import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";

import { createJournal } from "@/api/journal";

type JournalDialogProps = {
  open: boolean;
  onClose: () => void;
};

const schema = z.object({
  title: z.string().min(1, "Title is required"),
  content: z.string(),
});

type FormValues = z.infer<typeof schema>;

export default function JournalDialog({ open, onClose }: JournalDialogProps) {
  const {
    register,
    reset,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<FormValues>({
    resolver: zodResolver(schema),
  });

  const onSubmit = async (data: FormValues) => {
    try {
      await createJournal(data);

      reset();

      onClose();

      toast.success("Journal created successfully!");
    } catch (error) {
      toast.error("Failed to create journal.");
    }
  };

  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent>
        <form onSubmit={handleSubmit(onSubmit)} className="flex flex-col gap-4">
          <DialogHeader>
            <DialogTitle>Add Journal</DialogTitle>
          </DialogHeader>

          <div className="grid gap-3">
            <Label htmlFor="title">Title</Label>

            <Input id="title" {...register("title")} />

            {errors.title && (
              <p className="text-red-500 text-sm">{errors.title.message}</p>
            )}
          </div>

          <div className="grid gap-3">
            <Label htmlFor="content">Content</Label>

            <Textarea id="content" {...register("content")} rows={3} />

            {errors.content && (
              <p className="text-red-500 text-sm">{errors.content.message}</p>
            )}
          </div>

          <DialogFooter className="mt-2">
            <Button variant="outline" size="sm" onClick={onClose}>
              Cancel
            </Button>

            <Button type="submit" size="sm" disabled={isSubmitting}>
              Add
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}
