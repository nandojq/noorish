import { useDraggable } from "@dnd-kit/core";
import { CSS } from "@dnd-kit/utilities";
import { X, AlertTriangle } from "lucide-react";
import { Link } from "react-router-dom";
import { Badge } from "@/components/ui/badge";

const IMAGE_BASE = "http://localhost:8000/api/recipes";

function CardInner({ recipe, compact, onRemove }) {
  const imageUrl = recipe.imageId
    ? `${IMAGE_BASE}/${recipe.id}/image`
    : null;

  if (compact) {
    return (
      <div className="relative flex items-center gap-2 bg-light rounded-lg border border-border px-2 py-1.5 shadow-sm group">
        {imageUrl ? (
          <img
            src={imageUrl}
            alt={recipe.name}
            className="w-8 h-8 rounded object-cover shrink-0"
          />
        ) : (
          <div className="w-8 h-8 rounded bg-gradient-to-br from-accent/30 to-green/30 shrink-0" />
        )}
        <div className="flex-1 min-w-0">
          <p className="text-xs font-medium text-dark truncate">{recipe.name}</p>
          {recipe.nutritionPerServing?.calories != null && (
            <p className="text-xs text-dark/50">
              {Math.round(recipe.nutritionPerServing.calories)} kcal
            </p>
          )}
        </div>
        {recipe.status === "incomplete" && (
          <AlertTriangle size={12} className="text-deficient shrink-0" />
        )}
        {onRemove && (
          <button
            onClick={(e) => {
              e.stopPropagation();
              onRemove();
            }}
            className="opacity-0 group-hover:opacity-100 transition-opacity text-dark/40 hover:text-deficient ml-1 shrink-0"
            aria-label="Remove"
          >
            <X size={14} />
          </button>
        )}
      </div>
    );
  }

  return (
    <div className="bg-light rounded-xl border border-border shadow-sm overflow-hidden hover:shadow-md transition-shadow cursor-pointer">
      {imageUrl ? (
        <img
          src={imageUrl}
          alt={recipe.name}
          className="w-full h-40 object-cover"
        />
      ) : (
        <div className="w-full h-40 bg-gradient-to-br from-accent/20 to-green/20 flex items-center justify-center">
          <span className="text-3xl text-dark/20">🍽</span>
        </div>
      )}
      <div className="p-3">
        <div className="flex items-start justify-between gap-2">
          <h3 className="text-sm font-semibold text-dark leading-tight line-clamp-2">
            {recipe.name}
          </h3>
          {recipe.status === "incomplete" && (
            <Badge variant="destructive" className="shrink-0">Incomplete</Badge>
          )}
        </div>
        {recipe.tags?.length > 0 && (
          <p className="text-xs text-dark/50 mt-1 truncate">
            {recipe.tags.slice(0, 3).join(" · ")}
          </p>
        )}
        <div className="flex items-center justify-between mt-2">
          {recipe.nutritionPerServing?.calories != null ? (
            <span className="text-xs text-dark/60">
              {Math.round(recipe.nutritionPerServing.calories)} kcal / serving
            </span>
          ) : (
            <span className="text-xs text-dark/40">No nutrition data</span>
          )}
          <span className="text-xs text-dark/40">
            {recipe.prepTimeMinutes != null && recipe.cookTimeMinutes != null
              ? `${recipe.prepTimeMinutes + recipe.cookTimeMinutes} min`
              : ""}
          </span>
        </div>
      </div>
    </div>
  );
}

export default function RecipeCard({ recipe, draggable, onRemove, compact }) {
  const { attributes, listeners, setNodeRef, transform, isDragging } =
    useDraggable({
      id: `recipe-${recipe.id}`,
      data: { recipe },
      disabled: !draggable,
    });

  const style = draggable
    ? {
        transform: CSS.Translate.toString(transform),
        opacity: isDragging ? 0.4 : 1,
        cursor: "grab",
        zIndex: isDragging ? 999 : undefined,
      }
    : {};

  const inner = <CardInner recipe={recipe} compact={compact} onRemove={onRemove} />;

  if (draggable) {
    return (
      <div ref={setNodeRef} style={style} {...listeners} {...attributes}>
        {inner}
      </div>
    );
  }

  if (!compact) {
    return (
      <Link to={`/recipes/${recipe.id}`} className="block">
        {inner}
      </Link>
    );
  }

  return inner;
}
