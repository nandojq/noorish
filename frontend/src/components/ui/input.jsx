import { cn } from "@/lib/utils";

export function Input({ className, type = "text", style, ...props }) {
  return (
    <input
      type={type}
      className={cn(
        "flex h-9 w-full rounded-lg border border-kf-neutral-200 px-3 py-1 text-sm placeholder:text-text-placeholder focus:outline-none focus:ring-2 focus:ring-accent focus:border-accent disabled:opacity-50",
        className
      )}
      style={{ color: "var(--color-text-high)", background: "var(--color-surface-alt)", ...style }}
      {...props}
    />
  );
}
