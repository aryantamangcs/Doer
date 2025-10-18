import { ReactNode } from "react";

import { SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar";

import { Nav } from "./nav";

type LayoutProps = {
  children: ReactNode;
};

export default function Layout({ children }: LayoutProps) {
  return (
    <SidebarProvider>
      <Nav />

      <main className="w-full">
        <SidebarTrigger />

        {children}
      </main>
    </SidebarProvider>
  );
}
