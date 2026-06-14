import { useEffect } from "react";
import { X } from "lucide-react";
import { cn } from "@/lib/utils";

export function Dialog({ open, onClose, children }) {
  useEffect(() => {
    const handleKey = (e) => {
      if (e.key === "Escape" && open) onClose?.();
    };
    document.addEventListener("keydown", handleKey);
    return () => document.removeEventListener("keydown", handleKey);
  }, [open, onClose]);

  if (!open) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      <div
        className="absolute inset-0 bg-black/50"
        onClick={onClose}
      />
      <div className="relative z-10 w-full max-w-lg">{children}</div>
    </div>
  );
}

export function DialogContent({ className, children, onClose, ...props }) {
  return (
    <div
      className={cn(
        "relative bg-light rounded-xl border border-border p-6 max-h-[90vh] overflow-y-auto popover-shadow",
        className
      )}
      {...props}
    >
      {onClose && (
        <button
          onClick={onClose}
          className="absolute top-4 right-4 text-dark/40 hover:text-dark transition-colors"
        >
          <X size={18} />
        </button>
      )}
      {children}
    </div>
  );
}

export function DialogHeader({ className, ...props }) {
  return <div className={cn("mb-4", className)} {...props} />;
}

export function DialogTitle({ className, ...props }) {
  return (
    <h2 className={cn("text-lg font-bold text-dark", className)} {...props} />
  );
}

export function DialogDescription({ className, ...props }) {
  return (
    <p className={cn("text-sm text-dark/60 mt-1", className)} {...props} />
  );
}

export function DialogFooter({ className, ...props }) {
  return (
    <div
      className={cn("flex items-center justify-end gap-2 mt-6", className)}
      {...props}
    />
  );
}
