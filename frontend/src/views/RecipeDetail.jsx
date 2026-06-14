import { useState } from "react";
import { useParams, useNavigate, Link } from "react-router-dom";
import { Edit2, Trash2, AlertTriangle, Clock, Users, ExternalLink } from "lucide-react";
import { toast } from "sonner";
import { useRecipe, useDeleteRecipe } from "@/hooks/useRecipes";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import ConfirmDialog from "@/components/ConfirmDialog";
import { RECIPE_UNITS, INGREDIENT_CATEGORIES } from "@/lib/constants";

const IMAGE_BASE = "http://localhost:8000/api/recipes";

function MacroBar({ label, value, unit, color, total }) {
  const pct = total > 0 ? Math.min((value / total) * 100, 100) : 0;
  return (
    <div className="space-y-1">
      <div className="flex justify-between text-xs">
        <span className="text-dark/60">{label}</span>
        <span className="font-medium text-dark">
          {value?.toFixed(1)} {unit}
        </span>
      </div>
      <div className="h-1.5 bg-dark/10 rounded-full overflow-hidden">
        <div
          className="h-full rounded-full transition-all"
          style={{ width: `${pct}%`, backgroundColor: color }}
        />
      </div>
    </div>
  );
}

function getUnitLabel(value) {
  return RECIPE_UNITS.find((u) => u.value === value)?.label || value;
}

function getCategoryLabel(value) {
  return (
    INGREDIENT_CATEGORIES.find((c) => c.value === value)?.label || value
  );
}

export default function RecipeDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [deleteOpen, setDeleteOpen] = useState(false);
  const { data: recipe, isLoading, error } = useRecipe(id);
  const deleteRecipe = useDeleteRecipe();

  if (isLoading) {
    return (
      <div className="max-w-5xl mx-auto p-6 space-y-4">
        <Skeleton className="h-64 w-full rounded-xl" />
        <div className="grid grid-cols-2 gap-6">
          <Skeleton className="h-80 rounded-xl" />
          <Skeleton className="h-80 rounded-xl" />
        </div>
      </div>
    );
  }

  if (error || !recipe) {
    return (
      <div className="p-6 text-center">
        <p className="text-deficient">Recipe not found.</p>
        <Button variant="outline" className="mt-4" onClick={() => navigate("/recipes")}>
          Back to Recipes
        </Button>
      </div>
    );
  }

  const imageUrl = recipe.imageId ? `${IMAGE_BASE}/${recipe.id}/image` : null;
  const ns = recipe.nutritionPerServing;
  const totalMacros = ns
    ? (ns.macronutrients?.protein || 0) +
      (ns.macronutrients?.carbohydrates || 0) +
      (ns.macronutrients?.fat || 0)
    : 0;

  const handleDelete = () => {
    deleteRecipe.mutate(id, {
      onSuccess: () => {
        toast.success("Recipe deleted");
        navigate("/recipes");
      },
      onError: () => toast.error("Failed to delete recipe"),
    });
  };

  return (
    <div className="max-w-5xl mx-auto p-6">
      {/* Incomplete banner */}
      {recipe.status === "incomplete" && (
        <div className="flex items-center gap-3 bg-deficient/10 border border-deficient/30 rounded-xl p-4 mb-6">
          <AlertTriangle size={18} className="text-deficient shrink-0" />
          <p className="text-sm text-deficient">
            This recipe is missing ingredients and cannot be used in menus until fixed.
          </p>
        </div>
      )}

      {/* Header image */}
      <div className="relative rounded-xl overflow-hidden mb-6">
        {imageUrl ? (
          <img src={imageUrl} alt={recipe.name} className="w-full h-64 object-cover" />
        ) : (
          <div className="w-full h-64 bg-gradient-to-br from-accent/20 to-green/20" />
        )}
        <div className="absolute inset-0 bg-gradient-to-t from-dark/60 to-transparent" />
        <div className="absolute bottom-0 left-0 right-0 p-6 flex items-end justify-between">
          <div>
            <h1 className="text-2xl font-bold text-white">{recipe.name}</h1>
            {recipe.tags?.length > 0 && (
              <div className="flex gap-2 mt-2 flex-wrap">
                {recipe.tags.map((tag) => (
                  <Badge key={tag} variant="outline" className="border-white/40 text-white/80 bg-dark/20">
                    {tag}
                  </Badge>
                ))}
              </div>
            )}
          </div>
          <div className="flex gap-2">
            <Button
              size="sm"
              variant="secondary"
              onClick={() => navigate(`/recipes/${id}/edit`)}
            >
              <Edit2 size={14} />
              Edit
            </Button>
            <Button
              size="sm"
              variant="destructive"
              onClick={() => setDeleteOpen(true)}
            >
              <Trash2 size={14} />
              Delete
            </Button>
          </div>
        </div>
      </div>

      {/* Two-column layout */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left: Details */}
        <div className="lg:col-span-2 space-y-6">
          {/* Metadata */}
          <div className="bg-light rounded-xl border border-border p-4 flex flex-wrap gap-4">
            <div className="flex items-center gap-2 text-sm text-dark/60">
              <Users size={16} />
              <span>{recipe.servings} servings</span>
            </div>
            <div className="flex items-center gap-2 text-sm text-dark/60">
              <Clock size={16} />
              <span>Prep: {recipe.prepTimeMinutes} min</span>
            </div>
            <div className="flex items-center gap-2 text-sm text-dark/60">
              <Clock size={16} />
              <span>Cook: {recipe.cookTimeMinutes} min</span>
            </div>
            {recipe.metadata?.sourceUrl && (
              <a
                href={recipe.metadata.sourceUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center gap-1 text-sm text-accent hover:underline"
              >
                <ExternalLink size={14} />
                Source
              </a>
            )}
          </div>

          {/* Ingredients */}
          <div className="bg-light rounded-xl border border-border overflow-hidden">
            <div className="px-4 py-3 border-b border-border">
              <h2 className="font-semibold text-dark">Ingredients</h2>
            </div>
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-border bg-main/40">
                  <th className="text-left px-4 py-2 text-xs font-medium text-dark/60">Ingredient</th>
                  <th className="text-right px-4 py-2 text-xs font-medium text-dark/60">Amount</th>
                  <th className="text-left px-4 py-2 text-xs font-medium text-dark/60">Unit</th>
                </tr>
              </thead>
              <tbody>
                {recipe.ingredients?.map((ing, i) => (
                  <tr
                    key={i}
                    className={`border-b border-border/50 ${
                      !ing.ingredientId ? "bg-deficient/10" : ""
                    }`}
                  >
                    <td className="px-4 py-2 text-dark">
                      {ing.ingredientName}
                      {!ing.ingredientId && (
                        <Badge variant="destructive" className="ml-2 text-xs">Missing</Badge>
                      )}
                    </td>
                    <td className="px-4 py-2 text-right text-dark/80">{ing.amount}</td>
                    <td className="px-4 py-2 text-dark/60">{getUnitLabel(ing.unit)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Instructions */}
          {(recipe.cookInstructions?.length > 0 || recipe.prepInstructions?.length > 0) && (
            <div className="bg-light rounded-xl border border-border p-4 space-y-4">
              {recipe.prepInstructions?.length > 0 && (
                <div>
                  <h2 className="font-semibold text-dark mb-3">Prep Instructions</h2>
                  <ol className="space-y-2">
                    {recipe.prepInstructions.map((step, i) => (
                      <li key={i} className="flex gap-3 text-sm text-dark">
                        <span className="w-5 h-5 rounded-full bg-accent/20 text-accent text-xs font-bold flex items-center justify-center shrink-0 mt-0.5">
                          {i + 1}
                        </span>
                        {step}
                      </li>
                    ))}
                  </ol>
                </div>
              )}
              {recipe.cookInstructions?.length > 0 && (
                <div>
                  <h2 className="font-semibold text-dark mb-3">Cook Instructions</h2>
                  <ol className="space-y-2">
                    {recipe.cookInstructions.map((step, i) => (
                      <li key={i} className="flex gap-3 text-sm text-dark">
                        <span className="w-5 h-5 rounded-full bg-accent/20 text-accent text-xs font-bold flex items-center justify-center shrink-0 mt-0.5">
                          {i + 1}
                        </span>
                        {step}
                      </li>
                    ))}
                  </ol>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Right: Nutrition */}
        <div className="space-y-4">
          <div className="bg-light rounded-xl border border-border p-4">
            <h2 className="font-semibold text-dark mb-4">Nutrition per Serving</h2>
            {ns ? (
              <div className="space-y-4">
                <div className="text-center py-3 bg-main rounded-lg">
                  <p className="text-3xl font-bold text-dark">
                    {Math.round(ns.calories || 0)}
                  </p>
                  <p className="text-xs text-dark/60">calories</p>
                </div>
                <div className="space-y-3">
                  <MacroBar
                    label="Protein"
                    value={ns.macronutrients?.protein}
                    unit="g"
                    color="#12A99A"
                    total={totalMacros}
                  />
                  <MacroBar
                    label="Carbohydrates"
                    value={ns.macronutrients?.carbohydrates}
                    unit="g"
                    color="#E06620"
                    total={totalMacros}
                  />
                  <MacroBar
                    label="Fat"
                    value={ns.macronutrients?.fat}
                    unit="g"
                    color="#C93434"
                    total={totalMacros}
                  />
                  <MacroBar
                    label="Fiber"
                    value={ns.macronutrients?.fiber}
                    unit="g"
                    color="#12A99A"
                    total={28}
                  />
                </div>
              </div>
            ) : (
              <p className="text-sm text-dark/60 text-center py-4">
                No nutrition data available
              </p>
            )}
          </div>
        </div>
      </div>

      <ConfirmDialog
        open={deleteOpen}
        onClose={() => setDeleteOpen(false)}
        onConfirm={handleDelete}
        title={`Delete "${recipe.name}"?`}
        description="This recipe will be permanently deleted. Any menus using it will have this recipe removed."
      />
    </div>
  );
}
