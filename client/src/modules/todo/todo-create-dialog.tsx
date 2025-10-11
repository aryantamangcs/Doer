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
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

import { createTodo } from "@/api/todo";

import { TODO_STATUS_LIST } from "./constant";

import { Category } from "./types";

const categorySchema = z.object({
  title: z.string().min(1, "Title is required"),
  description: z.string().optional(),
  status: z.enum(["pending", "in_progress", "completed"]),
});

type TodoCategoryCreateDialogProps = {
  open: boolean;
  onClose: () => void;
  selectedCategory: Category;
};

type CategoryFormValues = z.infer<typeof categorySchema>;

export default function TodoCreateDialog({
  open,
  onClose,
  //
  selectedCategory,
}: TodoCategoryCreateDialogProps) {
  const {
    register,
    reset,
    handleSubmit,
    formState: { errors, isSubmitting },
    watch,
  } = useForm<CategoryFormValues>({
    resolver: zodResolver(categorySchema),
    defaultValues: {
      status: "pending",
    },
  });

  const onSubmit = async (data: CategoryFormValues) => {
    try {
      await createTodo({
        todo_list_identifier: selectedCategory.identifier,
        ...data,
      });

      toast.success("Todo created successfully!");

      reset();

      onClose();
    } catch (error) {
      console.error(error);

      toast.error("Failed to create category.");
    }
  };

  const selectedStatus = watch("status");

  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-sm">
        <form onSubmit={handleSubmit(onSubmit)} className="flex flex-col gap-4">
          <DialogHeader>
            <DialogTitle>Add Todo</DialogTitle>
          </DialogHeader>

          <div className="grid gap-3">
            <Label htmlFor="title">Title</Label>

            <Input id="title" {...register("title")} />

            {errors.title && (
              <p className="text-red-500 text-sm">{errors.title.message}</p>
            )}
          </div>

          <div className="grid gap-3">
            <Label htmlFor="description">Description</Label>

            <Textarea id="description" {...register("description")} rows={3} />
          </div>

          <div className="grid gap-3">
            <Label htmlFor="status">Status</Label>

            <Select
              value={selectedStatus}
              onValueChange={(value) => {
                const event = { target: { name: "status", value } } as any;
                register("status").onChange(event);
              }}
            >
              <SelectTrigger>
                <SelectValue placeholder="Select status" />
              </SelectTrigger>

              <SelectContent>
                {TODO_STATUS_LIST.map((status) => (
                  <SelectItem key={status.value} value={status.value}>
                    {status.label}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
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
