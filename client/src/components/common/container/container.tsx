import { ReactNode } from "react";

import { cn } from "@/lib/utils";

interface ContainerProps {
  className?: string;
  children: ReactNode;
}

export default function Container({ className, children }: ContainerProps) {
  return <div className={cn("p-4 w-full h-full", className)}>{children}</div>;
}
