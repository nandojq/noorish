import { cn } from "@/lib/utils";

export function Select({ className, children, ...props }) {
  return (
    <select
      className={cn(
        "flex h-9 w-full rounded-lg border border-border bg-light px-3 py-1 text-sm text-dark focus:outline-none focus:ring-2 focus:ring-accent focus:border-accent disabled:opacity-50",
        className
      )}
      {...props}
    >
      {children}
    </select>
  );
}
