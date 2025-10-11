import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

type TodoCategoryCreateDialogProps = {
  open: boolean;
  onClose: () => void;
};

export default function TodoCategoryCreateDialog({
  open,
  onClose,
}: TodoCategoryCreateDialogProps) {
  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-sm">
        <DialogHeader>
          <DialogTitle>Add Todo Category</DialogTitle>

          <DialogDescription>
            Add a category to better group and manage your todos.
          </DialogDescription>
        </DialogHeader>

        <div className="grid gap-3">
          <Label htmlFor="name">Name</Label>

          <Input id="name" name="name" />
        </div>

        <DialogFooter>
          <Button variant="outline" size="sm">
            Cancel
          </Button>

          <Button type="submit" size="sm">
            Add
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
