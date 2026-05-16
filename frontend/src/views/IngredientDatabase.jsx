import { useState } from "react";
import { toast } from "sonner";
import { Plus, MagnifyingGlass, Trash, ArrowClockwise } from "@phosphor-icons/react";
import {
  useIngredients, useDeleteIngredient,
  useSearchUSDA, useImportUSDA,
  useSearchOFF, useImportOFF,
  useCreateIngredient,
} from "@/hooks/useIngredients";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from "@/components/ui/dialog";
import { Skeleton } from "@/components/ui/skeleton";
import ConfirmDialog from "@/components/ConfirmDialog";
import EmptyState from "@/components/EmptyState";
import { INGREDIENT_CATEGORIES, DATA_QUALITY } from "@/lib/constants";

const IMAGE_BASE = "http://localhost:8000";

function QualityBadge({ quality }) {
  const map = {
    high:   { label: "High",   style: { background: "#D4EDE0", color: "#3A8A60" } },
    medium: { label: "Medium", style: { background: "#FAE2D0", color: "#9A5030" } },
    low:    { label: "Low",    style: { background: "#E8EEF0", color: "#5A7A85" } },
  };
  const { label, style } = map[quality] || map.low;
  return (
    <span className="text-xs font-medium px-2 py-0.5 rounded-full" style={style}>{label}</span>
  );
}

// ── Tab: USDA ──────────────────────────────────────────────────────────────────

function USDATab({ onSuccess }) {
  const [q, setQ] = useState("");
  const [submitted, setSubmitted] = useState("");
  const [selected, setSelected] = useState(null);
  const [nameOverride, setNameOverride] = useState("");
  const { data: results, isLoading, error } = useSearchUSDA(submitted);
  const importUSDA = useImportUSDA();

  const handleSearch = (e) => { e.preventDefault(); setSubmitted(q.trim()); setSelected(null); };

  const handleImport = () => {
    if (!selected) return;
    importUSDA.mutate(
      { fdcId: selected.fdcId, overrides: nameOverride ? { name: nameOverride } : {} },
      {
        onSuccess: (ing) => { toast.success(`"${ing.name}" imported`); onSuccess(); },
        onError: (err) => toast.error(err.data?.existingId ? "Ingredient already exists" : err.message),
      }
    );
  };

  return (
    <div className="space-y-4">
      <form onSubmit={handleSearch} className="flex gap-2">
        <Input value={q} onChange={(e) => setQ(e.target.value)} placeholder="Search USDA FoodData Central…" className="flex-1" />
        <Button type="submit" variant="outline" size="sm" disabled={!q.trim()}>
          <MagnifyingGlass size={14} />
          Search
        </Button>
      </form>
      {isLoading && <Skeleton className="h-32 w-full" />}
      {error && <p className="text-sm text-error">Search failed: {error.message}</p>}
      {results && (
        <div className="space-y-1 max-h-52 overflow-y-auto">
          {results.map((r) => (
            <button
              key={r.fdcId}
              onClick={() => { setSelected(r); setNameOverride(r.name); }}
              type="button"
              className="w-full text-left px-3 py-2 rounded-lg text-sm transition-colors"
              style={{
                background: selected?.fdcId === r.fdcId ? "var(--color-primary)" : "var(--color-surface)",
                color: selected?.fdcId === r.fdcId ? "#fff" : "var(--color-text-high)",
                boxShadow: "var(--shadow-raised-sm)",
              }}
            >
              <span className="font-medium">{r.name}</span>
              <span className="ml-2 text-xs opacity-70">{r.dataType}</span>
            </button>
          ))}
        </div>
      )}
      {selected && (
        <div className="space-y-2">
          <Label className="text-xs text-text-mid">Edit name before importing</Label>
          <Input value={nameOverride} onChange={(e) => setNameOverride(e.target.value)} />
          <Button onClick={handleImport} disabled={importUSDA.isPending} className="w-full">
            {importUSDA.isPending ? "Importing…" : `Import "${nameOverride || selected.name}"`}
          </Button>
        </div>
      )}
    </div>
  );
}

// ── Tab: Open Food Facts ───────────────────────────────────────────────────────

function OFFTab({ onSuccess }) {
  const [q, setQ] = useState("");
  const [submitted, setSubmitted] = useState("");
  const [selected, setSelected] = useState(null);
  const [nameOverride, setNameOverride] = useState("");
  const { data: results, isLoading, error } = useSearchOFF({ q: submitted });
  const importOFF = useImportOFF();

  const handleSearch = (e) => { e.preventDefault(); setSubmitted(q.trim()); setSelected(null); };

  const handleImport = () => {
    if (!selected) return;
    importOFF.mutate(
      { offId: selected.offId, overrides: nameOverride ? { name: nameOverride } : {} },
      {
        onSuccess: (ing) => { toast.success(`"${ing.name}" imported`); onSuccess(); },
        onError: (err) => toast.error(err.message),
      }
    );
  };

  return (
    <div className="space-y-4">
      <form onSubmit={handleSearch} className="flex gap-2">
        <Input value={q} onChange={(e) => setQ(e.target.value)} placeholder="Search Open Food Facts…" className="flex-1" />
        <Button type="submit" variant="outline" size="sm" disabled={!q.trim()}>
          <MagnifyingGlass size={14} />
          Search
        </Button>
      </form>
      {isLoading && <Skeleton className="h-32 w-full" />}
      {error && <p className="text-sm text-error">Search failed: {error.message}</p>}
      {results && (
        <div className="space-y-1 max-h-52 overflow-y-auto">
          {results.map((r) => (
            <button
              key={r.offId}
              onClick={() => { setSelected(r); setNameOverride(r.name); }}
              type="button"
              className="w-full text-left px-3 py-2 rounded-lg text-sm transition-colors"
              style={{
                background: selected?.offId === r.offId ? "var(--color-primary)" : "var(--color-surface)",
                color: selected?.offId === r.offId ? "#fff" : "var(--color-text-high)",
                boxShadow: "var(--shadow-raised-sm)",
              }}
            >
              <span className="font-medium">{r.name}</span>
            </button>
          ))}
        </div>
      )}
      {selected && (
        <div className="space-y-2">
          <Label className="text-xs text-text-mid">Edit name before importing</Label>
          <Input value={nameOverride} onChange={(e) => setNameOverride(e.target.value)} />
          <Button onClick={handleImport} disabled={importOFF.isPending} className="w-full">
            {importOFF.isPending ? "Importing…" : `Import "${nameOverride || selected.name}"`}
          </Button>
        </div>
      )}
    </div>
  );
}

// ── Tab: Manual ───────────────────────────────────────────────────────────────

const EMPTY_NUTRITION = {
  calories: "", protein: "", carbohydrates: "", fat: "",
  fiber: "", sugar: "", sodium: "", calcium: "", iron: "",
  vitaminC: "", vitaminA: "",
};

function ManualTab({ onSuccess }) {
  const createIngredient = useCreateIngredient();
  const [form, setForm] = useState({
    name: "", category: "vegetable", season: "all_year",
  });
  const [nutrition, setNutrition] = useState(EMPTY_NUTRITION);
  const [errors, setErrors] = useState({});

  const setF = (k, v) => setForm((p) => ({ ...p, [k]: v }));
  const setN = (k, v) => setNutrition((p) => ({ ...p, [k]: v }));

  const validate = () => {
    const errs = {};
    if (!form.name.trim()) errs.name = "Required";
    if (!nutrition.calories) errs.calories = "Required";
    if (!nutrition.protein) errs.protein = "Required";
    if (!nutrition.carbohydrates) errs.carbohydrates = "Required";
    if (!nutrition.fat) errs.fat = "Required";
    setErrors(errs);
    return Object.keys(errs).length === 0;
  };

  const handleCreate = () => {
    if (!validate()) return;
    const n = (k) => parseFloat(nutrition[k]) || 0;
    createIngredient.mutate(
      {
        name: form.name.trim(),
        category: form.category,
        season: form.season,
        nutritionPer100G: {
          calories: n("calories"),
          macronutrients: {
            protein: n("protein"), carbohydrates: n("carbohydrates"), fat: n("fat"),
            fiber: n("fiber"), sugar: n("sugar"),
            saturatedFat: 0, transFat: 0, polyunsaturatedFat: 0, monounsaturatedFat: 0,
            addedSugars: 0, cholesterol: 0,
          },
          micronutrients: {
            vitamins: { vitaminA: n("vitaminA"), vitaminC: n("vitaminC"), vitaminD: 0, vitaminE: 0, vitaminK: 0, thiamine: 0, riboflavin: 0, niacin: 0, vitaminB6: 0, folate: 0, vitaminB12: 0 },
            minerals: { calcium: n("calcium"), iron: n("iron"), magnesium: 0, phosphorus: 0, potassium: 0, zinc: 0, copper: 0, manganese: 0, selenium: 0, sodium: n("sodium") },
          },
        },
        metadata: {
          source: "manual",
          lastUpdated: new Date().toISOString(),
          dataQuality: "low",
        },
      },
      {
        onSuccess: (ing) => { toast.success(`"${ing.name}" created`); onSuccess(); },
        onError: (err) => toast.error(err.data?.existingId ? "Name already exists" : err.message),
      }
    );
  };

  const nField = (key, label, required) => (
    <div>
      <Label className="text-xs text-text-mid">{label}{required && <span className="text-error ml-0.5">*</span>}</Label>
      <Input type="number" min={0} step={0.01} value={nutrition[key]} onChange={(e) => setN(key, e.target.value)} className="mt-1" />
      {errors[key] && <p className="text-xs text-error mt-0.5">{errors[key]}</p>}
    </div>
  );

  return (
    <div className="space-y-4">
      <div>
        <Label className="text-xs text-text-mid">Name <span className="text-error">*</span></Label>
        <Input value={form.name} onChange={(e) => setF("name", e.target.value)} placeholder="e.g. Spinach" className="mt-1" />
        {errors.name && <p className="text-xs text-error mt-0.5">{errors.name}</p>}
      </div>
      <div className="grid grid-cols-2 gap-3">
        <div>
          <Label className="text-xs text-text-mid">Category</Label>
          <select value={form.category} onChange={(e) => setF("category", e.target.value)} className="w-full mt-1 h-9 text-sm rounded-lg border border-border bg-light px-2 focus:outline-none focus:ring-2 focus:ring-primary">
            {INGREDIENT_CATEGORIES.map((c) => <option key={c.value} value={c.value}>{c.label}</option>)}
          </select>
        </div>
        <div>
          <Label className="text-xs text-text-mid">Season</Label>
          <select value={form.season} onChange={(e) => setF("season", e.target.value)} className="w-full mt-1 h-9 text-sm rounded-lg border border-border bg-light px-2 focus:outline-none focus:ring-2 focus:ring-primary">
            {[{v:"all_year",l:"All Year"},{v:"winter",l:"Winter"},{v:"spring",l:"Spring"},{v:"summer",l:"Summer"},{v:"autumn",l:"Autumn"}].map(({v,l}) => <option key={v} value={v}>{l}</option>)}
          </select>
        </div>
      </div>

      <p className="text-xs font-medium text-text-mid uppercase tracking-wide">Macros per 100g</p>
      <div className="grid grid-cols-2 gap-3">
        {nField("calories", "Calories (kcal)", true)}
        {nField("protein", "Protein (g)", true)}
        {nField("carbohydrates", "Carbohydrates (g)", true)}
        {nField("fat", "Fat (g)", true)}
        {nField("fiber", "Fiber (g)")}
        {nField("sugar", "Sugar (g)")}
      </div>
      <p className="text-xs font-medium text-text-mid uppercase tracking-wide">Key micros (optional)</p>
      <div className="grid grid-cols-2 gap-3">
        {nField("sodium", "Sodium (mg)")}
        {nField("calcium", "Calcium (mg)")}
        {nField("iron", "Iron (mg)")}
        {nField("vitaminC", "Vitamin C (mg)")}
        {nField("vitaminA", "Vitamin A (mcg)")}
      </div>

      <Button onClick={handleCreate} disabled={createIngredient.isPending} className="w-full">
        {createIngredient.isPending ? "Creating…" : "Create Ingredient"}
      </Button>
    </div>
  );
}

// ── Add Modal ─────────────────────────────────────────────────────────────────

function AddIngredientModal({ open, onClose }) {
  const [activeTab, setActiveTab] = useState("usda");
  const tabs = [
    { key: "usda", label: "USDA" },
    { key: "off", label: "Open Food Facts" },
    { key: "manual", label: "Manual" },
  ];

  return (
    <Dialog open={open} onClose={onClose}>
      <DialogContent onClose={onClose} className="max-w-xl">
        <DialogHeader>
          <DialogTitle>Add Ingredient</DialogTitle>
        </DialogHeader>

        <div className="flex gap-1 mb-5 p-1 rounded-lg" style={{ background: "var(--color-surface-down)" }}>
          {tabs.map(({ key, label }) => (
            <button
              key={key}
              onClick={() => setActiveTab(key)}
              className="flex-1 py-1.5 text-sm font-medium rounded-md transition-all"
              style={{
                background: activeTab === key ? "var(--color-surface)" : "transparent",
                color: activeTab === key ? "var(--color-primary-dark)" : "var(--color-text-mid)",
                boxShadow: activeTab === key ? "var(--shadow-raised-sm)" : "none",
              }}
            >
              {label}
            </button>
          ))}
        </div>

        {activeTab === "usda"   && <USDATab   onSuccess={onClose} />}
        {activeTab === "off"    && <OFFTab    onSuccess={onClose} />}
        {activeTab === "manual" && <ManualTab onSuccess={onClose} />}
      </DialogContent>
    </Dialog>
  );
}

// ── Main View ─────────────────────────────────────────────────────────────────

export default function IngredientDatabase() {
  const [search, setSearch] = useState("");
  const [category, setCategory] = useState("");
  const [dataQuality, setDataQuality] = useState("");
  const [addOpen, setAddOpen] = useState(false);
  const [deleteTarget, setDeleteTarget] = useState(null);

  const { data: ingredients, isLoading, error } = useIngredients({
    search, category: category || undefined, dataQuality: dataQuality || undefined,
  });
  const deleteIngredient = useDeleteIngredient();

  const handleDelete = () => {
    if (!deleteTarget) return;
    deleteIngredient.mutate(deleteTarget.id, {
      onSuccess: () => { toast.success(`"${deleteTarget.name}" deleted`); setDeleteTarget(null); },
      onError: () => toast.error("Failed to delete"),
    });
  };

  return (
    <div className="max-w-7xl mx-auto p-6">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold text-dark" style={{ fontFamily: "var(--font-display)" }}>
          Ingredients
        </h1>
        <button onClick={() => setAddOpen(true)} className="btn-primary flex items-center gap-2">
          <Plus size={16} />
          Add Ingredient
        </button>
      </div>

      {/* Filters */}
      <div className="flex flex-wrap gap-3 mb-6">
        <div className="relative flex-1 min-w-48">
          <MagnifyingGlass size={14} className="absolute left-3 top-1/2 -translate-y-1/2 text-text-low" />
          <Input
            placeholder="Search by name or alias…"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="pl-8"
          />
        </div>
        <select
          value={category}
          onChange={(e) => setCategory(e.target.value)}
          className="h-9 text-sm rounded-lg border border-border bg-light px-3 focus:outline-none focus:ring-2 focus:ring-primary"
        >
          <option value="">All categories</option>
          {INGREDIENT_CATEGORIES.map((c) => <option key={c.value} value={c.value}>{c.label}</option>)}
        </select>
        <select
          value={dataQuality}
          onChange={(e) => setDataQuality(e.target.value)}
          className="h-9 text-sm rounded-lg border border-border bg-light px-3 focus:outline-none focus:ring-2 focus:ring-primary"
        >
          <option value="">All quality</option>
          {DATA_QUALITY.map((q) => <option key={q.value} value={q.value}>{q.label}</option>)}
        </select>
      </div>

      {/* Table */}
      {isLoading ? (
        <div className="space-y-2">
          {Array.from({ length: 8 }).map((_, i) => <Skeleton key={i} className="h-12 w-full" />)}
        </div>
      ) : error ? (
        <p className="text-sm text-error text-center py-8">Failed to load ingredients.</p>
      ) : !ingredients?.length ? (
        <EmptyState
          title="No ingredients found"
          description={search || category || dataQuality ? "Try changing your filters." : "Add your first ingredient to get started."}
          action={!search && !category && !dataQuality ? { label: "Add an ingredient", onClick: () => setAddOpen(true) } : undefined}
        />
      ) : (
        <div className="rounded-xl overflow-hidden" style={{ background: "var(--color-surface)", boxShadow: "var(--shadow-raised)" }}>
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-border" style={{ background: "var(--color-surface-down)" }}>
                {["Name", "Category", "Cal/100g", "Protein", "Fat", "Carbs", "Source", "Quality", ""].map((h) => (
                  <th key={h} className="text-left px-4 py-3 text-xs font-semibold text-text-mid">{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {ingredients.map((ing, i) => {
                const n = ing.nutritionPer100G || ing.nutritionPer100g || {};
                const macros = n.macronutrients || {};
                return (
                  <tr
                    key={ing.id}
                    className="border-b border-border/40 last:border-none hover:bg-primary/5 transition-colors"
                  >
                    <td className="px-4 py-3 font-medium text-dark">{ing.name}</td>
                    <td className="px-4 py-3 text-text-mid capitalize">{ing.category?.replace(/_/g, " ")}</td>
                    <td className="px-4 py-3 data-value text-dark" style={{ fontFamily: "var(--font-mono)" }}>
                      {Math.round(n.calories || 0)}
                    </td>
                    <td className="px-4 py-3 text-text-mid">{(macros.protein || 0).toFixed(1)}g</td>
                    <td className="px-4 py-3 text-text-mid">{(macros.fat || 0).toFixed(1)}g</td>
                    <td className="px-4 py-3 text-text-mid">{(macros.carbohydrates || 0).toFixed(1)}g</td>
                    <td className="px-4 py-3 text-text-low text-xs">{ing.metadata?.source || "—"}</td>
                    <td className="px-4 py-3">
                      <QualityBadge quality={ing.metadata?.dataQuality} />
                    </td>
                    <td className="px-4 py-3">
                      <button
                        onClick={() => setDeleteTarget(ing)}
                        className="text-text-low hover:text-error transition-colors"
                        aria-label="Delete"
                      >
                        <Trash size={15} />
                      </button>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
          <div className="px-4 py-2 border-t border-border text-xs text-text-low">
            {ingredients.length} ingredient{ingredients.length !== 1 ? "s" : ""}
          </div>
        </div>
      )}

      <AddIngredientModal open={addOpen} onClose={() => setAddOpen(false)} />

      <ConfirmDialog
        open={!!deleteTarget}
        onClose={() => setDeleteTarget(null)}
        onConfirm={handleDelete}
        title={`Delete "${deleteTarget?.name}"?`}
        description="Recipes using this ingredient will be marked incomplete."
      />
    </div>
  );
}
