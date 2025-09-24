import Link from "next/link";

import { Button } from "@/components/ui/button";

interface AuthPromptProps {
  content: string;
  title: string;
  href: string;
}

export default function AuthPrompt({ content, title, href }: AuthPromptProps) {
  return (
    <div className="flex gap-3 items-center justify-end w-full bg-white md:bg-transparent p-4">
      <p className="text-sm text-muted-foreground"> {content} </p>

      <Button
        asChild
        variant="outline"
        className="rounded-full hover:cursor-pointer"
      >
        <Link href={href}> {title} </Link>
      </Button>
    </div>
  );
}
