"use client";

import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

import { Container } from "@/components/common";

import { signUp } from "@/api/auth";

import { AuthPrompt, InfoPanel } from "../components";

const signUpSchema = z
  .object({
    firstName: z.string().min(2, "First name must be at least 2 characters"),
    lastName: z.string().min(2, "Last name must be at least 2 characters"),
    username: z.string().min(2, "Username must be at least 2 characters"),
    email: z.string().email("Invalid email"),
    password: z.string().min(6, "Password must be at least 6 characters"),
    confirmPassword: z.string().min(6, "Confirm password must match"),
  })
  .refine((data) => data.password === data.confirmPassword, {
    message: "Passwords do not match",
    path: ["confirmPassword"],
  });

type SignUpFormValues = z.infer<typeof signUpSchema>;

export function SignupView() {
  const prompt = {
    content: "Already have an account?",
    title: "Sign in",
    href: "/auth/signin",
  };

  return (
    <div className="h-screen flex">
      <InfoPanel className="hidden md:flex" />

      <section className="w-full fixed top-0 right-0">
        <AuthPrompt {...prompt} />
      </section>

      <SignupForm />
    </div>
  );
}

function SignupForm() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<SignUpFormValues>({
    resolver: zodResolver(signUpSchema),
  });

  const onSubmit = async (data: SignUpFormValues) => {
    try {
      const response = await signUp({
        first_name: data.firstName,
        last_name: data.lastName,
        username: data.username,
        email: data.email,
        password: data.password,
      });

      console.log("Sign up success:", response);
    } catch (error) {
      console.error("Sign up failed:", error);
    }
  };

  return (
    <Container>
      <div className="h-full w-full flex items-center justify-center">
        <div className="w-full max-w-[400px] flex flex-col gap-6">
          <header className="flex flex-col gap-1">
            <h3 className="text-2xl font-semibold"> Create Account </h3>

            <p className="text-xs text-muted-foreground">
              Your productivity journey starts here
            </p>
          </header>

          <form
            onSubmit={handleSubmit(onSubmit)}
            className="flex flex-col gap-6"
          >
            <div className="flex gap-10">
              <div className="flex flex-col gap-1">
                <Label htmlFor="firstName" className="text-gray-500">
                  First Name
                </Label>

                <Input
                  id="firstName"
                  type="text"
                  {...register("firstName")}
                  aria-invalid={!!errors.firstName}
                  className="rounded-none border-0 shadow-none border-b border-gray-300 focus-visible:ring-0 focus:border-black"
                />

                {errors.firstName && (
                  <p className="text-red-500 text-sm">
                    {errors.firstName.message}
                  </p>
                )}
              </div>

              <div className="flex flex-col gap-1">
                <Label htmlFor="lastName" className="text-gray-500">
                  Last Name
                </Label>

                <Input
                  id="lastName"
                  type="text"
                  {...register("lastName")}
                  aria-invalid={!!errors.lastName}
                  className="rounded-none border-0 shadow-none border-b border-gray-300 focus-visible:ring-0 focus:border-black"
                />

                {errors.lastName && (
                  <p className="text-red-500 text-sm">
                    {errors.lastName.message}
                  </p>
                )}
              </div>
            </div>

            <div className="flex flex-col gap-1">
              <Label htmlFor="username" className="text-gray-500">
                Username
              </Label>

              <Input
                id="username"
                type="text"
                {...register("username")}
                aria-invalid={!!errors.username}
                className="rounded-none border-0 shadow-none border-b border-gray-300 focus-visible:ring-0 focus:border-black"
              />

              {errors.username && (
                <p className="text-red-500 text-sm">
                  {errors.username.message}
                </p>
              )}
            </div>

            <div className="flex flex-col gap-1">
              <Label htmlFor="email" className="text-gray-500">
                Email
              </Label>

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

              <Input
                id="password"
                type="password"
                {...register("password")}
                aria-invalid={!!errors.password}
                className="rounded-none border-0 shadow-none border-b border-gray-300 focus-visible:ring-0 focus:border-black"
              />

              {errors.password && (
                <p className="text-red-500 text-sm">
                  {errors.password.message}
                </p>
              )}
            </div>

            <div className="flex flex-col gap-1">
              <Label htmlFor="confirmPassword" className="text-gray-500">
                Confirm Password
              </Label>

              <Input
                id="confirmPassword"
                type="password"
                {...register("confirmPassword")}
                aria-invalid={!!errors.confirmPassword}
                className="rounded-none border-0 shadow-none border-b border-gray-300 focus-visible:ring-0 focus:border-black"
              />

              {errors.confirmPassword && (
                <p className="text-red-500 text-sm">
                  {errors.confirmPassword.message}
                </p>
              )}
            </div>

            <Button type="submit" className="mt-6" disabled={isSubmitting}>
              Sign up
            </Button>
          </form>
        </div>
      </div>
    </Container>
  );
}
