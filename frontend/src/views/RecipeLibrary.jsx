import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Plus, Search } from "lucide-react";
import { useRecipes } from "@/hooks/useRecipes";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Skeleton } from "@/components/ui/skeleton";
import RecipeCard from "@/components/RecipeCard";
import EmptyState from "@/components/EmptyState";

const FILTER_CHIPS = [
  { key: "seasonal", label: "Seasonal" },
  { key: "quick", label: "Quick" },
  { key: "vegetarian", label: "Vegetarian" },
  { key: "incomplete", label: "Incomplete" },
];

export default function RecipeLibrary() {
  const navigate = useNavigate();
  const [search, setSearch] = useState("");
  const [activeFilters, setActiveFilters] = useState([]);

  const isIncompleteFilter = activeFilters.includes("incomplete");
  const { data: recipes, isLoading, error } = useRecipes({
    search,
    status: isIncompleteFilter ? "incomplete" : undefined,
  });

  const toggleFilter = (key) => {
    setActiveFilters((prev) =>
      prev.includes(key) ? prev.filter((f) => f !== key) : [...prev, key]
    );
  };

  const filteredRecipes = recipes?.filter((r) => {
    if (activeFilters.includes("quick")) {
      const total = (r.prepTimeMinutes || 0) + (r.cookTimeMinutes || 0);
      if (total > 30) return false;
    }
    if (activeFilters.includes("vegetarian")) {
      if (!r.tags?.some((t) => ["vegetarian", "vegan"].includes(t.toLowerCase())))
        return false;
    }
    if (activeFilters.includes("seasonal")) {
      if (!r.tags?.some((t) => t.toLowerCase() === "seasonal")) return false;
    }
    return true;
  });

  return (
    <div className="p-6 max-w-7xl mx-auto">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold text-dark">Recipes</h1>
        <Button onClick={() => navigate("/recipes/new")}>
          <Plus size={16} />
          New Recipe
        </Button>
      </div>

      {/* Search + filters */}
      <div className="flex flex-col gap-3 mb-6">
        <div className="relative">
          <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-dark/40" />
          <Input
            placeholder="Search recipes..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="pl-9"
          />
        </div>
        <div className="flex gap-2 flex-wrap">
          {FILTER_CHIPS.map(({ key, label }) => (
            <button
              key={key}
              onClick={() => toggleFilter(key)}
              className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${
                activeFilters.includes(key)
                  ? "bg-accent text-light border-accent"
                  : "bg-transparent text-dark/60 border-border hover:border-accent/50"
              }`}
            >
              {label}
            </button>
          ))}
        </div>
      </div>

      {error && (
        <p className="text-sm text-deficient text-center py-8">
          Failed to load recipes. Please try again.
        </p>
      )}

      {isLoading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {Array.from({ length: 6 }).map((_, i) => (
            <Skeleton key={i} className="h-56 w-full rounded-xl" />
          ))}
        </div>
      ) : filteredRecipes?.length === 0 ? (
        <EmptyState
          title="No recipes yet"
          description={
            search || activeFilters.length
              ? "No recipes match your current filters."
              : "Start building your recipe library."
          }
          action={
            !search && !activeFilters.length
              ? { label: "Create your first recipe", onClick: () => navigate("/recipes/new") }
              : undefined
          }
        />
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {filteredRecipes?.map((recipe) => (
            <RecipeCard key={recipe.id} recipe={recipe} />
          ))}
        </div>
      )}
    </div>
  );
}
