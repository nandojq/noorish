import { useState, useEffect, useCallback, useRef } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { toast } from "sonner";
import {
  Plus, Trash, ArrowLeft, Image, MagnifyingGlass,
} from "@phosphor-icons/react";
import { useRecipe, useCreateRecipe, useUpdateRecipe, useUploadRecipeImage } from "@/hooks/useRecipes";
import { useIngredients } from "@/hooks/useIngredients";
import { apiFetch } from "@/api/client";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Skeleton } from "@/components/ui/skeleton";
import { INGREDIENT_CATEGORIES, RECIPE_UNITS, SEASONS } from "@/lib/constants";

const IMAGE_BASE = "http://localhost:8000/api/recipes";

// Debounce helper
function useDebounce(value, ms = 300) {
  const [deb, setDeb] = useState(value);
  useEffect(() => {
    const t = setTimeout(() => setDeb(value), ms);
    return () => clearTimeout(t);
  }, [value, ms]);
  return deb;
}

function IngredientSearch({ onSelect }) {
  const [query, setQuery] = useState("");
  const debounced = useDebounce(query, 250);
  const [open, setOpen] = useState(false);
  const { data: results } = useIngredients({ search: debounced });
  const ref = useRef(null);

  useEffect(() => {
    function handler(e) {
      if (ref.current && !ref.current.contains(e.target)) setOpen(false);
    }
    document.addEventListener("mousedown", handler);
    return () => document.removeEventListener("mousedown", handler);
  }, []);

  return (
    <div className="relative" ref={ref}>
      <div className="relative">
        <MagnifyingGlass size={14} className="absolute left-3 top-1/2 -translate-y-1/2 text-text-low" />
        <Input
          placeholder="Search ingredient…"
          value={query}
          onChange={(e) => { setQuery(e.target.value); setOpen(true); }}
          onFocus={() => setOpen(true)}
          className="pl-8 text-sm"
        />
      </div>
      {open && debounced && results?.length > 0 && (
        <div
          className="absolute z-20 left-0 right-0 top-full mt-1 rounded-lg overflow-hidden shadow-lg border border-border"
          style={{ background: "var(--color-surface)", maxHeight: 220, overflowY: "auto" }}
        >
          {results.map((ing) => (
            <button
              key={ing.id}
              type="button"
              onClick={() => {
                onSelect(ing);
                setQuery("");
                setOpen(false);
              }}
              className="w-full text-left px-3 py-2 text-sm hover:bg-primary/10 transition-colors"
            >
              <span className="font-medium text-dark">{ing.name}</span>
              <span className="text-xs text-text-low ml-2">{ing.category}</span>
            </button>
          ))}
        </div>
      )}
      {open && debounced && results?.length === 0 && (
        <div className="absolute z-20 left-0 right-0 top-full mt-1 rounded-lg border border-border px-3 py-2 text-xs text-text-low" style={{ background: "var(--color-surface)" }}>
          No ingredients found
        </div>
      )}
    </div>
  );
}

function SectionCard({ title, children }) {
  return (
    <div className="rounded-xl overflow-hidden" style={{ background: "var(--color-surface)", boxShadow: "var(--shadow-raised)" }}>
      <div className="px-6 py-4 border-b border-border">
        <h2 className="font-semibold text-dark" style={{ fontFamily: "var(--font-display)", fontSize: "1.05rem" }}>{title}</h2>
      </div>
      <div className="px-6 py-5">{children}</div>
    </div>
  );
}

function Field({ label, required, error, children }) {
  return (
    <div className="space-y-1">
      <Label className="text-xs font-medium text-text-mid">
        {label}{required && <span className="text-error ml-0.5">*</span>}
      </Label>
      {children}
      {error && <p className="text-xs text-error">{error}</p>}
    </div>
  );
}

function NeuTextarea({ value, onChange, placeholder, rows = 3 }) {
  return (
    <textarea
      value={value}
      onChange={onChange}
      placeholder={placeholder}
      rows={rows}
      className="w-full text-sm text-dark rounded-lg border border-border bg-light resize-none px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary placeholder:text-text-low"
      style={{ boxShadow: "var(--shadow-inset-sm)" }}
    />
  );
}

function NeuSelect({ value, onChange, children }) {
  return (
    <select
      value={value}
      onChange={onChange}
      className="w-full h-9 text-sm text-dark rounded-lg border border-border bg-light px-3 focus:outline-none focus:ring-2 focus:ring-primary"
      style={{ boxShadow: "var(--shadow-inset-sm)" }}
    >
      {children}
    </select>
  );
}

export default function RecipeForm() {
  const { id } = useParams();
  const navigate = useNavigate();
  const isEdit = !!id;

  const { data: existing, isLoading: existingLoading } = useRecipe(isEdit ? id : null);
  const createRecipe = useCreateRecipe();
  const updateRecipe = useUpdateRecipe();
  const uploadImage = useUploadRecipeImage(id);

  const [form, setForm] = useState({
    name: "",
    description: "",
    servings: 2,
    prepTimeMinutes: 0,
    cookTimeMinutes: 0,
    tags: "",
    sourceUrl: "",
  });
  const [ingredients, setIngredients] = useState([]);
  const [cookInstructions, setCookInstructions] = useState([""]);
  const [prepInstructions, setPrepInstructions] = useState([]);
  const [imageFile, setImageFile] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [preview, setPreview] = useState(null);
  const [errors, setErrors] = useState({});

  // Pre-fill form when editing
  useEffect(() => {
    if (existing && isEdit) {
      setForm({
        name: existing.name || "",
        description: existing.description || "",
        servings: existing.servings || 2,
        prepTimeMinutes: existing.prepTimeMinutes ?? 0,
        cookTimeMinutes: existing.cookTimeMinutes ?? 0,
        tags: (existing.tags || []).join(", "),
        sourceUrl: existing.sourceUrl || "",
      });
      setIngredients(
        (existing.ingredients || []).map((ing) => ({
          ingredientId: ing.ingredientId,
          ingredientName: ing.ingredientName || "",
          amount: ing.amount,
          unit: ing.unit,
        }))
      );
      setCookInstructions(existing.cookInstructions?.length ? existing.cookInstructions : [""]);
      setPrepInstructions(existing.prepInstructions || []);
      if (existing.imageId) setImagePreview(`${IMAGE_BASE}/${existing.id}/image`);
    }
  }, [existing, isEdit]);

  // Live nutrition preview
  useEffect(() => {
    const validIngredients = ingredients.filter(
      (i) => i.ingredientId && i.amount > 0
    );
    if (!validIngredients.length || !form.servings) { setPreview(null); return; }
    const timeout = setTimeout(async () => {
      try {
        const data = await apiFetch("/recipes/preview", {
          method: "POST",
          body: JSON.stringify({
            name: "preview",
            servings: Number(form.servings) || 1,
            cookInstructions: ["preview"],
            ingredients: validIngredients.map((i) => ({
              ingredientId: i.ingredientId,
              amount: i.amount,
              unit: i.unit,
            })),
          }),
        });
        setPreview(data);
      } catch {}
    }, 600);
    return () => clearTimeout(timeout);
  }, [ingredients, form.servings]);

  const addIngredient = (ing) => {
    setIngredients((prev) => [
      ...prev,
      { ingredientId: ing.id, ingredientName: ing.name, amount: 100, unit: "grams" },
    ]);
  };

  const updateIngredient = (idx, field, value) => {
    setIngredients((prev) =>
      prev.map((row, i) => (i === idx ? { ...row, [field]: value } : row))
    );
  };

  const removeIngredient = (idx) =>
    setIngredients((prev) => prev.filter((_, i) => i !== idx));

  const updateInstruction = (list, setList, idx, value) => {
    setList(list.map((s, i) => (i === idx ? value : s)));
  };

  const addInstruction = (list, setList) => setList([...list, ""]);

  const removeInstruction = (list, setList, idx) =>
    setList(list.filter((_, i) => i !== idx));

  const validate = () => {
    const errs = {};
    if (!form.name.trim()) errs.name = "Name is required";
    if (!form.servings || form.servings < 1) errs.servings = "Must be at least 1";
    if (!ingredients.length) errs.ingredients = "At least one ingredient is required";
    if (!cookInstructions.some((s) => s.trim())) errs.cookInstructions = "At least one cook instruction is required";
    setErrors(errs);
    return Object.keys(errs).length === 0;
  };

  const handleImageChange = (e) => {
    const file = e.target.files?.[0];
    if (!file) return;
    if (!["image/jpeg", "image/png", "image/webp"].includes(file.type)) {
      toast.error("Only JPEG, PNG, or WebP accepted");
      return;
    }
    if (file.size > 5 * 1024 * 1024) {
      toast.error("Image must be under 5MB");
      return;
    }
    setImageFile(file);
    setImagePreview(URL.createObjectURL(file));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validate()) return;

    const payload = {
      name: form.name.trim(),
      description: form.description.trim() || null,
      servings: Number(form.servings),
      prepTimeMinutes: Number(form.prepTimeMinutes) || 0,
      cookTimeMinutes: Number(form.cookTimeMinutes) || 0,
      tags: form.tags.split(",").map((t) => t.trim()).filter(Boolean),
      sourceUrl: form.sourceUrl.trim() || null,
      cookInstructions: cookInstructions.filter((s) => s.trim()),
      prepInstructions: prepInstructions.filter((s) => s.trim()),
      ingredients: ingredients.map((i) => ({
        ingredientId: i.ingredientId,
        ingredientName: i.ingredientName,
        amount: Number(i.amount),
        unit: i.unit,
      })),
    };

    const mutation = isEdit
      ? (data) => updateRecipe.mutateAsync({ id, ...data })
      : createRecipe.mutateAsync;

    try {
      const result = await mutation(payload);
      const savedId = result?.id || id;

      if (imageFile && savedId) {
        try {
          const formData = new FormData();
          formData.append("file", imageFile);
          await apiFetch(`/recipes/${savedId}/image`, { method: "POST", headers: {}, body: formData });
        } catch {}
      }

      toast.success(isEdit ? "Recipe updated" : "Recipe created");
      navigate(`/recipes/${savedId}`);
    } catch (err) {
      toast.error(err.message || "Failed to save recipe");
    }
  };

  if (isEdit && existingLoading) {
    return (
      <div className="max-w-3xl mx-auto p-6 space-y-4">
        <Skeleton className="h-8 w-48" />
        <Skeleton className="h-64 w-full" />
      </div>
    );
  }

  const ns = preview?.nutritionPerServing;

  return (
    <form onSubmit={handleSubmit} className="max-w-3xl mx-auto p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center gap-4">
        <button type="button" onClick={() => navigate(isEdit ? `/recipes/${id}` : "/recipes")} className="icon-btn">
          <ArrowLeft size={18} />
        </button>
        <h1 className="text-2xl font-bold text-dark" style={{ fontFamily: "var(--font-display)" }}>
          {isEdit ? "Edit Recipe" : "New Recipe"}
        </h1>
      </div>

      {/* Basic Info */}
      <SectionCard title="Basic Info">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="md:col-span-2">
            <Field label="Recipe name" required error={errors.name}>
              <Input
                value={form.name}
                onChange={(e) => setForm({ ...form, name: e.target.value })}
                placeholder="e.g. Moroccan Chickpea Stew"
              />
            </Field>
          </div>
          <div className="md:col-span-2">
            <Field label="Description">
              <NeuTextarea
                value={form.description}
                onChange={(e) => setForm({ ...form, description: e.target.value })}
                placeholder="Brief description…"
                rows={2}
              />
            </Field>
          </div>
          <Field label="Servings" required error={errors.servings}>
            <Input
              type="number"
              min={1}
              value={form.servings}
              onChange={(e) => setForm({ ...form, servings: e.target.value })}
            />
          </Field>
          <Field label="Tags (comma-separated)">
            <Input
              value={form.tags}
              onChange={(e) => setForm({ ...form, tags: e.target.value })}
              placeholder="vegan, high-protein, quick"
            />
          </Field>
          <Field label="Prep time (min)">
            <Input
              type="number"
              min={0}
              value={form.prepTimeMinutes}
              onChange={(e) => setForm({ ...form, prepTimeMinutes: e.target.value })}
            />
          </Field>
          <Field label="Cook time (min)">
            <Input
              type="number"
              min={0}
              value={form.cookTimeMinutes}
              onChange={(e) => setForm({ ...form, cookTimeMinutes: e.target.value })}
            />
          </Field>
          <div className="md:col-span-2">
            <Field label="Source URL">
              <Input
                type="url"
                value={form.sourceUrl}
                onChange={(e) => setForm({ ...form, sourceUrl: e.target.value })}
                placeholder="https://…"
              />
            </Field>
          </div>
        </div>
      </SectionCard>

      {/* Image */}
      <SectionCard title="Image">
        <div className="flex items-start gap-4">
          <div
            className="w-24 h-24 rounded-lg overflow-hidden shrink-0"
            style={{ boxShadow: "var(--shadow-inset-sm)", background: "var(--color-surface-down)" }}
          >
            {imagePreview ? (
              <img src={imagePreview} alt="preview" className="w-full h-full object-cover" />
            ) : (
              <div className="w-full h-full flex items-center justify-center">
                <Image size={24} style={{ color: "var(--color-text-low)" }} />
              </div>
            )}
          </div>
          <div className="flex-1">
            <p className="text-xs text-text-mid mb-2">JPEG, PNG or WebP · Max 5 MB</p>
            <label
              className="inline-flex items-center gap-2 text-sm font-medium cursor-pointer px-4 py-2 rounded-pill"
              style={{ background: "var(--color-surface)", boxShadow: "var(--shadow-raised-sm)", color: "var(--color-text-mid)", borderRadius: "var(--radius-pill)" }}
            >
              <Image size={14} />
              Choose image
              <input type="file" accept="image/jpeg,image/png,image/webp" onChange={handleImageChange} className="sr-only" />
            </label>
            {imagePreview && (
              <button
                type="button"
                onClick={() => { setImageFile(null); setImagePreview(null); }}
                className="ml-3 text-xs text-error hover:underline"
              >
                Remove
              </button>
            )}
          </div>
        </div>
      </SectionCard>

      {/* Ingredients */}
      <SectionCard title={`Ingredients${ingredients.length ? ` (${ingredients.length})` : ""}`}>
        {errors.ingredients && <p className="text-xs text-error mb-3">{errors.ingredients}</p>}

        {ingredients.length > 0 && (
          <div className="space-y-2 mb-4">
            {ingredients.map((ing, idx) => (
              <div
                key={idx}
                className="flex items-center gap-2 p-2 rounded-lg"
                style={{ background: "var(--color-surface)", boxShadow: "var(--shadow-raised-sm)" }}
              >
                <span className="flex-1 text-sm font-medium text-dark truncate">{ing.ingredientName}</span>
                <input
                  type="number"
                  value={ing.amount}
                  onChange={(e) => updateIngredient(idx, "amount", e.target.value)}
                  className="w-20 text-sm text-center rounded-md border border-border bg-light h-7 px-2 focus:outline-none focus:ring-2 focus:ring-primary"
                  min={0}
                  step={0.1}
                />
                <select
                  value={ing.unit}
                  onChange={(e) => updateIngredient(idx, "unit", e.target.value)}
                  className="text-sm rounded-md border border-border bg-light h-7 px-2 focus:outline-none focus:ring-2 focus:ring-primary"
                >
                  {RECIPE_UNITS.map((u) => (
                    <option key={u.value} value={u.value}>{u.label}</option>
                  ))}
                </select>
                <button
                  type="button"
                  onClick={() => removeIngredient(idx)}
                  className="text-text-low hover:text-error transition-colors"
                >
                  <Trash size={14} />
                </button>
              </div>
            ))}
          </div>
        )}

        <IngredientSearch onSelect={addIngredient} />
      </SectionCard>

      {/* Instructions */}
      <SectionCard title="Instructions">
        {prepInstructions.length > 0 && (
          <div className="mb-4">
            <p className="text-xs font-medium text-text-mid uppercase tracking-wide mb-2">Prep</p>
            {prepInstructions.map((step, idx) => (
              <div key={idx} className="flex gap-2 mb-2 items-start">
                <span className="w-5 h-5 rounded-full text-xs font-bold flex items-center justify-center shrink-0 mt-1.5" style={{ background: "var(--color-secondary)", color: "#fff" }}>{idx + 1}</span>
                <NeuTextarea value={step} onChange={(e) => updateInstruction(prepInstructions, setPrepInstructions, idx, e.target.value)} rows={2} />
                <button type="button" onClick={() => removeInstruction(prepInstructions, setPrepInstructions, idx)} className="text-text-low hover:text-error mt-1.5 shrink-0"><Trash size={14} /></button>
              </div>
            ))}
          </div>
        )}
        <button type="button" onClick={() => addInstruction(prepInstructions, setPrepInstructions)} className="text-xs text-text-mid hover:text-primary flex items-center gap-1 mb-6">
          <Plus size={12} /> Add prep step
        </button>

        <p className="text-xs font-medium text-text-mid uppercase tracking-wide mb-2">Cook{" "}<span className="text-error">*</span></p>
        {errors.cookInstructions && <p className="text-xs text-error mb-2">{errors.cookInstructions}</p>}
        {cookInstructions.map((step, idx) => (
          <div key={idx} className="flex gap-2 mb-2 items-start">
            <span className="w-5 h-5 rounded-full text-xs font-bold flex items-center justify-center shrink-0 mt-1.5" style={{ background: "var(--color-accent)", color: "#fff" }}>{idx + 1}</span>
            <NeuTextarea value={step} onChange={(e) => updateInstruction(cookInstructions, setCookInstructions, idx, e.target.value)} rows={2} />
            {cookInstructions.length > 1 && (
              <button type="button" onClick={() => removeInstruction(cookInstructions, setCookInstructions, idx)} className="text-text-low hover:text-error mt-1.5 shrink-0"><Trash size={14} /></button>
            )}
          </div>
        ))}
        <button type="button" onClick={() => addInstruction(cookInstructions, setCookInstructions)} className="text-xs text-text-mid hover:text-primary flex items-center gap-1">
          <Plus size={12} /> Add cook step
        </button>
      </SectionCard>

      {/* Nutrition preview */}
      {ns && (
        <div className="rounded-xl p-4" style={{ background: "var(--color-surface)", boxShadow: "var(--shadow-raised)" }}>
          <p className="text-xs font-medium text-text-mid uppercase tracking-wide mb-3">Live nutrition preview (per serving)</p>
          <div className="grid grid-cols-4 gap-3">
            {[
              { label: "Calories", value: Math.round(ns.calories || 0), unit: "kcal" },
              { label: "Protein", value: (ns.macronutrients?.protein || 0).toFixed(1), unit: "g" },
              { label: "Carbs", value: (ns.macronutrients?.carbohydrates || 0).toFixed(1), unit: "g" },
              { label: "Fat", value: (ns.macronutrients?.fat || 0).toFixed(1), unit: "g" },
            ].map(({ label, value, unit }) => (
              <div key={label} className="text-center py-2 rounded-lg" style={{ background: "var(--color-surface)", boxShadow: "var(--shadow-inset-sm)" }}>
                <p className="data-value text-lg font-bold text-dark" style={{ fontFamily: "var(--font-mono)" }}>{value}</p>
                <p className="text-xs text-text-low">{unit}</p>
                <p className="text-xs text-text-mid">{label}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Actions */}
      <div className="flex items-center justify-end gap-3 pt-2">
        <Button
          type="button"
          variant="outline"
          onClick={() => navigate(isEdit ? `/recipes/${id}` : "/recipes")}
        >
          Cancel
        </Button>
        <button
          type="submit"
          disabled={createRecipe.isPending || updateRecipe.isPending}
          className="btn-primary disabled:opacity-50"
        >
          {createRecipe.isPending || updateRecipe.isPending ? "Saving…" : isEdit ? "Save Changes" : "Create Recipe"}
        </button>
      </div>
    </form>
  );
}
