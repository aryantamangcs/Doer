import { Home, ListTodo, BookOpenText } from "lucide-react";

import { paths } from "@/routes/paths";

export const navData = [
  {
    title: "Home",
    url: paths.home,
    icon: Home,
  },
  {
    title: "Todo",
    url: paths.todo,
    icon: ListTodo,
  },
  {
    title: "Journal",
    url: paths.journal,
    icon: BookOpenText,
  },
];
