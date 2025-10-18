"use client";

import { z } from "zod";
import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";

import { Eye, EyeOff } from "lucide-react";
import { toast } from "sonner";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Checkbox } from "@/components/ui/checkbox";
import { Label } from "@/components/ui/label";

import { Container } from "@/components/common";

import { signIn } from "@/api/auth";

import { paths } from "@/routes/paths";
import { useRouter } from "@/routes/hooks";

import { AuthPrompt, InfoPanel } from "../components";

const signInSchema = z.object({
  email: z.string().email("Invalid email"),
  password: z.string().min(6, "Password must be at least 6 characters"),
});

type SignInFormValues = z.infer<typeof signInSchema>;

export function SignInView() {
  const prompt = {
    content: "Don't have an account?",
    title: "Sign up",
    href: paths.auth.signUp,
  };

  return (
    <div className="h-screen flex">
      <InfoPanel className="hidden md:flex" />

      <section className="w-full fixed top-0 right-0">
        <AuthPrompt {...prompt} />
      </section>

      <SigninForm />
    </div>
  );
}

function SigninForm() {
  const [showPassword, setShowPassword] = useState<boolean>(false);
  const router = useRouter();

  const {
    register,
    reset,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<SignInFormValues>({
    resolver: zodResolver(signInSchema),
  });

  const onSubmit = async (data: SignInFormValues) => {
    try {
      const response = await signIn(data);

      reset();

      router.push(paths.todo);

      toast.success("Logged in successfully!");
    } catch (error) {
      console.error("Login failed:", error);
    }
  };

  return (
    <Container>
      <div className="h-full w-full flex items-center justify-center">
        <div className="w-full max-w-[400px]">
          <form
            onSubmit={handleSubmit(onSubmit)}
            className="flex flex-col gap-6"
          >
            <h6 className="font-semibold text-2xl"> Login to DOER </h6>

            <div className="flex flex-col gap-1">
              <Label htmlFor="email">Email</Label>

              <Input
                id="email"
                type="email"
                {...register("email")}
                aria-invalid={!!errors.email}
                className="rounded-none border-0 shadow-none border-b border-gray-300 focus-visible:ring-0 focus:border-black"
              />

              {errors.email && (
                <p className="text-red-500 text-sm">{errors.email.message}</p>
              )}
            </div>

            <div className="flex flex-col gap-1">
              <Label htmlFor="password" className="text-gray-500">
                Password
              </Label>

              <div className="relative">
                <Input
                  id="password"
                  type={showPassword ? "text" : "password"}
                  {...register("password")}
                  aria-invalid={!!errors.password}
                  className="rounded-none border-0 shadow-none border-b border-gray-300 focus-visible:ring-0 focus:border-black pr-10"
                />

                <button
                  type="button"
                  onClick={() => setShowPassword((prev) => !prev)}
                  className="absolute inset-y-0 right-0 flex items-center text-gray-500 hover:text-black"
                >
                  {showPassword ? <Eye size={18} /> : <EyeOff size={18} />}
                </button>
              </div>

              {errors.password && (
                <p className="text-red-500 text-sm">
                  {errors.password.message}
                </p>
              )}
            </div>

            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <Checkbox />

                <p className="text-sm"> Remember me </p>
              </div>

              <a
                href="#"
                className="text-muted-foreground text-sm underline-offset-4 hover:underline hover:text-gray-700 transition-colors duration-200"
              >
                Forgot your password?
              </a>
            </div>

            <Button
              type="submit"
              className="w-full mt-6"
              disabled={isSubmitting}
            >
              {isSubmitting ? "Logging in..." : "Login"}
            </Button>
          </form>
        </div>
      </div>
    </Container>
  );
}
