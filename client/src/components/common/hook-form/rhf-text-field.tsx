import { Controller, useFormContext } from "react-hook-form";

import { cn } from "@/lib/utils";

import { Input } from "@/components/ui/input";

type RHFTextFieldProps = {
  name: string;
  type?: string;
  placeholder?: string;
  className?: string;
};

export default function RHFTextField({
  name,
  type = "text",
  placeholder,
  className,
  ...other
}: RHFTextFieldProps) {
  const { control } = useFormContext();

  return (
    <Controller
      name={name}
      control={control}
      render={({ field, fieldState: { error } }) => (
        <div>
          <Input
            {...field}
            id={name}
            type={type}
            placeholder={placeholder}
            className={cn(
              "shadow-none border-b focus-visible:ring-0",
              className
            )}
            {...other}
          />

          {error && (
            <p className="text-red-500 text-sm mt-1">{error.message}</p>
          )}
        </div>
      )}
    />
  );
}
