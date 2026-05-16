import { useState, useMemo } from "react";
import { useParams, useNavigate, Link } from "react-router-dom";
import {
  DndContext,
  DragOverlay,
  PointerSensor,
  useSensor,
  useSensors,
  useDroppable,
} from "@dnd-kit/core";
import { toast } from "sonner";
import { ChevronLeft, ChevronRight, Plus, BarChart2, ShoppingCart, X } from "lucide-react";
import { useMenus, useMenu, useCreateMenu, useUpdateMenu, useDeleteMenu } from "@/hooks/useMenus";
import { useRecipes } from "@/hooks/useRecipes";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from "@/components/ui/dialog";
import { Skeleton } from "@/components/ui/skeleton";
import EmptyState from "@/components/EmptyState";
import RecipeCard from "@/components/RecipeCard";
import ConfirmDialog from "@/components/ConfirmDialog";
import { MEAL_TYPES } from "@/lib/constants";

const DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];

function getWeekDates(weekOffset, startDate) {
  const base = startDate ? new Date(startDate) : new Date();
  const dayOfWeek = base.getDay();
  const diffToMonday = (dayOfWeek === 0 ? -6 : 1 - dayOfWeek);
  const monday = new Date(base);
  monday.setDate(base.getDate() + diffToMonday + weekOffset * 7);
  return Array.from({ length: 7 }, (_, i) => {
    const d = new Date(monday);
    d.setDate(monday.getDate() + i);
    return d;
  });
}

function toISODate(date) {
  return date.toISOString().slice(0, 10);
}

function DroppableCell({ id, children, hasItems }) {
  const { isOver, setNodeRef } = useDroppable({ id });
  return (
    <div
      ref={setNodeRef}
      className={`min-h-[60px] rounded-lg border transition-colors p-1 space-y-1 ${
        isOver
          ? "border-accent border-dashed bg-accent/10"
          : hasItems
          ? "border-border bg-white/30"
          : "border-dashed border-border/60 bg-white/10 hover:border-accent/50"
      }`}
    >
      {children}
    </div>
  );
}

function NewMenuModal({ open, onClose, onCreate }) {
  const [form, setForm] = useState({ name: "", startDate: "", endDate: "" });
  const [errors, setErrors] = useState({});

  const validate = () => {
    const e = {};
    if (!form.name.trim()) e.name = "Name required";
    if (!form.startDate) e.startDate = "Start date required";
    if (!form.endDate) e.endDate = "End date required";
    if (form.startDate && form.endDate && form.endDate < form.startDate)
      e.endDate = "End date must be after start date";
    setErrors(e);
    return Object.keys(e).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!validate()) return;
    onCreate(form);
    setForm({ name: "", startDate: "", endDate: "" });
  };

  return (
    <Dialog open={open} onClose={onClose}>
      <DialogContent onClose={onClose}>
        <DialogHeader>
          <DialogTitle>New Menu</DialogTitle>
        </DialogHeader>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-1">
            <Label htmlFor="menu-name">Name</Label>
            <Input
              id="menu-name"
              value={form.name}
              onChange={(e) => setForm({ ...form, name: e.target.value })}
              placeholder="Weekly menu"
            />
            {errors.name && <p className="text-xs text-deficient">{errors.name}</p>}
          </div>
          <div className="grid grid-cols-2 gap-3">
            <div className="space-y-1">
              <Label htmlFor="start-date">Start Date</Label>
              <Input
                id="start-date"
                type="date"
                value={form.startDate}
                onChange={(e) => setForm({ ...form, startDate: e.target.value })}
              />
              {errors.startDate && (
                <p className="text-xs text-deficient">{errors.startDate}</p>
              )}
            </div>
            <div className="space-y-1">
              <Label htmlFor="end-date">End Date</Label>
              <Input
                id="end-date"
                type="date"
                value={form.endDate}
                onChange={(e) => setForm({ ...form, endDate: e.target.value })}
              />
              {errors.endDate && (
                <p className="text-xs text-deficient">{errors.endDate}</p>
              )}
            </div>
          </div>
          <DialogFooter>
            <Button type="button" variant="outline" onClick={onClose}>
              Cancel
            </Button>
            <Button type="submit">Create</Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}

export default function MenuPlanner() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [weekOffset, setWeekOffset] = useState(0);
  const [sidebarSearch, setSidebarSearch] = useState("");
  const [newMenuOpen, setNewMenuOpen] = useState(false);
  const [deleteMenuOpen, setDeleteMenuOpen] = useState(false);
  const [activeRecipe, setActiveRecipe] = useState(null);

  const { data: menus, isLoading: menusLoading } = useMenus();
  const currentMenuId = id || menus?.[0]?.id;
  const { data: menu, isLoading: menuLoading } = useMenu(currentMenuId);
  const { data: allRecipes, isLoading: recipesLoading } = useRecipes({ status: "complete" });
  const createMenu = useCreateMenu();
  const updateMenu = useUpdateMenu();
  const deleteMenu = useDeleteMenu();

  const sensors = useSensors(
    useSensor(PointerSensor, { activationConstraint: { distance: 5 } })
  );

  const weekDates = useMemo(() => {
    const base = menu?.startDate;
    return getWeekDates(weekOffset, base);
  }, [weekOffset, menu?.startDate]);

  const filteredRecipes = useMemo(() => {
    if (!allRecipes) return [];
    const q = sidebarSearch.toLowerCase();
    return q ? allRecipes.filter((r) => r.name.toLowerCase().includes(q)) : allRecipes;
  }, [allRecipes, sidebarSearch]);

  const getAssignedRecipes = (date, mealType) => {
    if (!menu?.days) return [];
    const day = menu.days.find((d) => d.date === date);
    if (!day) return [];
    const ids = day.meals?.[mealType] || [];
    return ids
      .map((rid) => allRecipes?.find((r) => r.id === rid))
      .filter(Boolean);
  };

  const handleDragStart = ({ active }) => {
    const recipe = active.data.current?.recipe;
    if (recipe) setActiveRecipe(recipe);
  };

  const handleDragEnd = ({ active, over }) => {
    setActiveRecipe(null);
    if (!over || !menu) return;

    const [dateStr, mealType] = over.id.split("__");
    const recipe = active.data.current?.recipe;
    if (!recipe) return;

    const updatedDays = [...(menu.days || [])];
    let day = updatedDays.find((d) => d.date === dateStr);
    if (!day) {
      day = { date: dateStr, meals: { breakfast: [], lunch: [], dinner: [], snack: [] } };
      updatedDays.push(day);
    }
    const meals = { ...day.meals };
    meals[mealType] = [...(meals[mealType] || []), recipe.id];
    const idx = updatedDays.indexOf(day);
    updatedDays[idx] = { ...day, meals };

    updateMenu.mutate(
      { id: menu.id, days: updatedDays },
      {
        onSuccess: () => toast.success("Menu updated"),
        onError: () => toast.error("Failed to update menu"),
      }
    );
  };

  const removeRecipe = (dateStr, mealType, recipeId) => {
    if (!menu) return;
    const updatedDays = (menu.days || []).map((day) => {
      if (day.date !== dateStr) return day;
      const meals = { ...day.meals };
      meals[mealType] = (meals[mealType] || []).filter((id) => id !== recipeId);
      return { ...day, meals };
    });
    updateMenu.mutate(
      { id: menu.id, days: updatedDays },
      {
        onSuccess: () => toast.success("Recipe removed"),
        onError: () => toast.error("Failed to update menu"),
      }
    );
  };

  const handleCreateMenu = (form) => {
    createMenu.mutate(
      { name: form.name, startDate: form.startDate, endDate: form.endDate },
      {
        onSuccess: (created) => {
          setNewMenuOpen(false);
          toast.success("Menu created");
          navigate(`/menus/${created.id}`);
        },
        onError: (err) => toast.error(err.message || "Failed to create menu"),
      }
    );
  };

  const handleDeleteMenu = () => {
    if (!menu) return;
    deleteMenu.mutate(menu.id, {
      onSuccess: () => {
        toast.success("Menu deleted");
        navigate("/menus");
      },
      onError: () => toast.error("Failed to delete menu"),
    });
  };

  if (menusLoading) {
    return (
      <div className="p-6 space-y-4">
        <Skeleton className="h-10 w-64" />
        <Skeleton className="h-80 w-full" />
      </div>
    );
  }

  if (!menus?.length && !menusLoading) {
    return (
      <div className="p-6">
        <EmptyState
          title="No menus yet"
          description="Create your first weekly menu to start planning meals."
          action={{ label: "Create a Menu", onClick: () => setNewMenuOpen(true) }}
        />
        <NewMenuModal
          open={newMenuOpen}
          onClose={() => setNewMenuOpen(false)}
          onCreate={handleCreateMenu}
        />
      </div>
    );
  }

  return (
    <DndContext
      sensors={sensors}
      onDragStart={handleDragStart}
      onDragEnd={handleDragEnd}
    >
      <div className="flex h-[calc(100vh-56px)]">
        {/* Main area */}
        <div className="flex-1 flex flex-col overflow-hidden">
          {/* Subheader */}
          <div className="bg-light border-b border-border px-4 py-3 flex items-center gap-3 flex-wrap">
            <select
              value={currentMenuId || ""}
              onChange={(e) => navigate(`/menus/${e.target.value}`)}
              className="h-8 rounded-lg border border-border bg-white text-sm text-dark px-2 focus:outline-none focus:ring-2 focus:ring-accent"
            >
              {menus?.map((m) => (
                <option key={m.id} value={m.id}>
                  {m.name}
                </option>
              ))}
            </select>
            <Button
              size="sm"
              variant="outline"
              onClick={() => setNewMenuOpen(true)}
            >
              <Plus size={14} />
              New Menu
            </Button>
            <div className="flex-1" />
            {currentMenuId && (
              <>
                <Button
                  size="sm"
                  variant="outline"
                  onClick={() => navigate(`/analysis/${currentMenuId}`)}
                >
                  <BarChart2 size={14} />
                  View Nutrition
                </Button>
                <Button
                  size="sm"
                  variant="outline"
                  onClick={() => navigate(`/grocery/${currentMenuId}`)}
                >
                  <ShoppingCart size={14} />
                  Grocery List
                </Button>
                <Button
                  size="sm"
                  variant="ghost"
                  className="text-deficient hover:text-deficient"
                  onClick={() => setDeleteMenuOpen(true)}
                >
                  Delete Menu
                </Button>
              </>
            )}
          </div>

          {/* Week navigation */}
          <div className="bg-white/40 border-b border-border px-4 py-2 flex items-center gap-4">
            <button
              onClick={() => setWeekOffset((o) => o - 1)}
              className="text-dark/60 hover:text-dark transition-colors"
            >
              <ChevronLeft size={18} />
            </button>
            <div className="flex gap-2 text-xs text-dark/60 font-medium">
              {weekDates.map((d) => (
                <span key={d.toISOString()} className="w-[80px] text-center">
                  {DAYS[d.getDay() === 0 ? 6 : d.getDay() - 1]}{" "}
                  {d.getDate()}/{d.getMonth() + 1}
                </span>
              ))}
            </div>
            <button
              onClick={() => setWeekOffset((o) => o + 1)}
              className="text-dark/60 hover:text-dark transition-colors"
            >
              <ChevronRight size={18} />
            </button>
          </div>

          {/* Grid */}
          <div className="flex-1 overflow-auto">
            {menuLoading ? (
              <div className="p-4 space-y-3">
                {MEAL_TYPES.map((mt) => (
                  <Skeleton key={mt.value} className="h-20 w-full" />
                ))}
              </div>
            ) : (
              <table className="w-full border-collapse text-sm">
                <tbody>
                  {MEAL_TYPES.map((mt) => (
                    <tr key={mt.value} className="border-b border-border/50">
                      <td className="w-24 px-3 py-2 text-xs font-semibold text-dark/60 bg-white/20 border-r border-border/50 sticky left-0">
                        {mt.label}
                      </td>
                      {weekDates.map((date) => {
                        const dateStr = toISODate(date);
                        const cellId = `${dateStr}__${mt.value}`;
                        const assigned = getAssignedRecipes(dateStr, mt.value);
                        return (
                          <td key={dateStr} className="p-1 w-[calc((100%-96px)/7)]">
                            <DroppableCell id={cellId} hasItems={assigned.length > 0}>
                              {assigned.map((recipe) => (
                                <RecipeCard
                                  key={recipe.id}
                                  recipe={recipe}
                                  compact
                                  draggable
                                  onRemove={() => removeRecipe(dateStr, mt.value, recipe.id)}
                                />
                              ))}
                              {!assigned.length && (
                                <div className="flex items-center justify-center h-10 text-dark/20">
                                  <Plus size={14} />
                                </div>
                              )}
                            </DroppableCell>
                          </td>
                        );
                      })}
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        </div>

        {/* Recipe Sidebar */}
        <aside className="w-64 bg-light border-l border-border flex flex-col">
          <div className="p-3 border-b border-border">
            <p className="text-xs font-semibold text-dark/60 mb-2">RECIPES</p>
            <Input
              placeholder="Search recipes..."
              value={sidebarSearch}
              onChange={(e) => setSidebarSearch(e.target.value)}
              className="text-xs h-8"
            />
          </div>
          <div className="flex-1 overflow-y-auto p-2 space-y-2">
            {recipesLoading ? (
              Array.from({ length: 6 }).map((_, i) => (
                <Skeleton key={i} className="h-16 w-full" />
              ))
            ) : filteredRecipes.length === 0 ? (
              <p className="text-xs text-dark/40 text-center py-4">
                {sidebarSearch ? "No matches" : "No complete recipes"}
              </p>
            ) : (
              filteredRecipes.map((recipe) => (
                <RecipeCard
                  key={recipe.id}
                  recipe={recipe}
                  draggable
                  compact
                />
              ))
            )}
          </div>
          <div className="p-3 border-t border-border">
            <Button
              size="sm"
              variant="outline"
              className="w-full"
              onClick={() => navigate("/recipes/new")}
            >
              <Plus size={14} />
              New Recipe
            </Button>
          </div>
        </aside>
      </div>

      <DragOverlay>
        {activeRecipe ? (
          <RecipeCard recipe={activeRecipe} compact />
        ) : null}
      </DragOverlay>

      <NewMenuModal
        open={newMenuOpen}
        onClose={() => setNewMenuOpen(false)}
        onCreate={handleCreateMenu}
      />

      <ConfirmDialog
        open={deleteMenuOpen}
        onClose={() => setDeleteMenuOpen(false)}
        onConfirm={handleDeleteMenu}
        title={`Delete "${menu?.name}"?`}
        description="This menu will be permanently deleted. Your recipes will not be affected."
      />
    </DndContext>
  );
}
