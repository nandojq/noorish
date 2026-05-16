import { cva } from "class-variance-authority";
import { cn } from "@/lib/utils";

const badgeVariants = cva(
  "inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium",
  {
    variants: {
      variant: {
        default: "bg-accent/20 text-accent",
        success: "bg-green/20 text-green",
        destructive: "bg-deficient/20 text-deficient",
        outline: "border border-border text-dark/60",
        secondary: "bg-dark/10 text-dark",
      },
    },
    defaultVariants: {
      variant: "default",
    },
  }
);

export function Badge({ className, variant, ...props }) {
  return (
    <span className={cn(badgeVariants({ variant }), className)} {...props} />
  );
}
