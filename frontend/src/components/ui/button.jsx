import { cva } from "class-variance-authority";
import { cn } from "@/lib/utils";

const buttonVariants = cva(
  "inline-flex items-center justify-center gap-2 rounded-lg text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent disabled:pointer-events-none disabled:opacity-50",
  {
    variants: {
      variant: {
        default: "bg-accent text-light hover:bg-accent/90 shadow-[var(--shadow-button)]",
        outline:
          "border border-kf-neutral-200 bg-transparent hover:bg-border/40",
        destructive: "bg-deficient text-white hover:bg-deficient/90",
        ghost: "bg-transparent hover:bg-border/40",
        secondary: "border border-kf-neutral-200 hover:bg-border/40",
      },
      size: {
        default: "h-9 px-4 py-2",
        sm: "h-7 px-3 text-xs",
        lg: "h-11 px-6 text-base",
        icon: "h-9 w-9",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
);

export function Button({ className, variant, size, style, ...props }) {
  return (
    <button
      className={cn(buttonVariants({ variant, size }), className)}
      style={{ color: "var(--color-text-high)", ...style }}
      {...props}
    />
  );
}

export { buttonVariants };
