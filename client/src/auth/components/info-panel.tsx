import { cn } from "@/lib/utils";

interface InfoPanelProps {
  className?: string;
}

export default function InfoPanel({ className }: InfoPanelProps) {
  return (
    <div
      className={cn(
        "h-full w-full bg-black flex flex-col gap-5 justify-center items-center text-white",
        className
      )}
    >
      <h1 className="text-5xl"> DOER </h1>

      <p className="text-xl text-gray-400">
        Your all-in-one productivity companion.
      </p>
    </div>
  );
}
