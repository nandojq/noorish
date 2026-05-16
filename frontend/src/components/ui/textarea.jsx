import { cn } from "@/lib/utils";

export function Textarea({ className, ...props }) {
  return (
    <textarea
      className={cn(
        "flex min-h-[80px] w-full rounded-lg border border-border bg-light px-3 py-2 text-sm text-dark placeholder:text-dark/40 focus:outline-none focus:ring-2 focus:ring-accent focus:border-accent disabled:opacity-50 resize-y",
        className
      )}
      {...props}
    />
  );
}
