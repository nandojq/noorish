import { Leaf } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Link } from "react-router-dom";

export default function EmptyState({ title, description, action }) {
  return (
    <div className="flex flex-col items-center justify-center py-20 px-6 text-center">
      <div className="w-16 h-16 rounded-full bg-accent/10 flex items-center justify-center mb-4">
        <Leaf size={28} className="text-accent" />
      </div>
      <h3 className="text-lg font-bold text-dark mb-2">{title}</h3>
      {description && (
        <p className="text-sm text-dark/60 max-w-sm mb-6">{description}</p>
      )}
      {action && (
        <>
          {action.href ? (
            <Button as={Link} to={action.href} onClick={action.onClick}>
              {action.label}
            </Button>
          ) : (
            <Button onClick={action.onClick}>{action.label}</Button>
          )}
        </>
      )}
    </div>
  );
}
