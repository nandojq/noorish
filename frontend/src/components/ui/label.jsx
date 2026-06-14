import { cn } from "@/lib/utils";

export function Label({ className, style, ...props }) {
  return (
    <label
      className={cn("text-sm font-medium", className)}
      style={{ color: "var(--color-text-high)", ...style }}
      {...props}
    />
  );
}
