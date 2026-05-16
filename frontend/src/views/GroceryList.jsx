import { useParams, useNavigate, Link } from "react-router-dom";
import { ArrowLeft, ShoppingCart, Export } from "@phosphor-icons/react";
import { useGroceryList } from "@/hooks/useMenus";
import { useMenus } from "@/hooks/useMenus";
import { Skeleton } from "@/components/ui/skeleton";
import EmptyState from "@/components/EmptyState";
import { INGREDIENT_CATEGORIES } from "@/lib/constants";

function getCategoryLabel(value) {
  return INGREDIENT_CATEGORIES.find((c) => c.value === value)?.label || value;
}

function exportAsText(items, menuName) {
  const grouped = groupByCategory(items);
  const lines = [`Grocery List — ${menuName}`, "=".repeat(40), ""];
  for (const [cat, catItems] of Object.entries(grouped)) {
    lines.push(`[ ${getCategoryLabel(cat)} ]`);
    for (const item of catItems) {
      lines.push(`  ${item.ingredientName}: ${item.totalGrams.toFixed(0)}g`);
    }
    lines.push("");
  }
  const blob = new Blob([lines.join("\n")], { type: "text/plain" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "grocery-list.txt";
  a.click();
  URL.revokeObjectURL(url);
}

function exportAsCSV(items) {
  const header = "Name,Category,Total (g)";
  const rows = items.map(
    (i) => `"${i.ingredientName}","${getCategoryLabel(i.category)}",${i.totalGrams.toFixed(0)}`
  );
  const blob = new Blob([[header, ...rows].join("\n")], { type: "text/csv" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "grocery-list.csv";
  a.click();
  URL.revokeObjectURL(url);
}

function groupByCategory(items) {
  return items.reduce((acc, item) => {
    const cat = item.category || "other";
    if (!acc[cat]) acc[cat] = [];
    acc[cat].push(item);
    return acc;
  }, {});
}

export default function GroceryList() {
  const { menuId } = useParams();
  const navigate = useNavigate();
  const { data: menus } = useMenus();
  const { data: grocery, isLoading, error } = useGroceryList(menuId);

  const currentMenu = menus?.find((m) => m.id === menuId);
  const grouped = grocery?.items ? groupByCategory(grocery.items) : {};
  const categoryOrder = INGREDIENT_CATEGORIES.map((c) => c.value);
  const sortedCategories = Object.keys(grouped).sort(
    (a, b) => categoryOrder.indexOf(a) - categoryOrder.indexOf(b)
  );

  if (isLoading) {
    return (
      <div className="max-w-3xl mx-auto p-6 space-y-4">
        <Skeleton className="h-8 w-64" />
        {Array.from({ length: 5 }).map((_, i) => (
          <Skeleton key={i} className="h-12 w-full" />
        ))}
      </div>
    );
  }

  if (error?.status === 422) {
    return (
      <div className="p-6">
        <EmptyState
          title="No ingredients to list"
          description="Assign recipes to your menu to generate a grocery list."
          action={{ label: "Go to Menu Planner", onClick: () => navigate(`/menus/${menuId}`) }}
        />
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6 text-center">
        <p className="text-sm" style={{ color: "var(--color-error)" }}>Failed to load grocery list.</p>
      </div>
    );
  }

  return (
    <div className="max-w-3xl mx-auto p-6">
      {/* Header */}
      <div className="flex items-center gap-4 mb-6">
        <button onClick={() => navigate(`/menus/${menuId}`)} className="icon-btn" aria-label="Back">
          <ArrowLeft size={18} />
        </button>
        <div className="flex-1">
          <h1 className="text-2xl font-bold text-dark" style={{ fontFamily: "var(--font-display)" }}>
            Grocery List
          </h1>
          {currentMenu && (
            <p className="text-sm text-text-mid mt-0.5">{currentMenu.name}</p>
          )}
        </div>
        {grocery?.items?.length > 0 && (
          <div className="flex gap-2">
            <button
              onClick={() => exportAsText(grocery.items, currentMenu?.name || "Menu")}
              className="flex items-center gap-1.5 text-xs font-medium text-text-mid hover:text-primary transition-colors px-3 py-2 rounded-lg"
              style={{ boxShadow: "var(--shadow-raised-sm)", background: "var(--color-surface)" }}
            >
              <Export size={14} />
              TXT
            </button>
            <button
              onClick={() => exportAsCSV(grocery.items)}
              className="flex items-center gap-1.5 text-xs font-medium text-text-mid hover:text-primary transition-colors px-3 py-2 rounded-lg"
              style={{ boxShadow: "var(--shadow-raised-sm)", background: "var(--color-surface)" }}
            >
              <Export size={14} />
              CSV
            </button>
          </div>
        )}
      </div>

      {!grocery?.items?.length ? (
        <EmptyState
          title="No ingredients to list"
          description="Assign recipes to your menu to generate a grocery list."
          action={{ label: "Go to Menu Planner", onClick: () => navigate(`/menus/${menuId}`) }}
        />
      ) : (
        <div className="space-y-4">
          {sortedCategories.map((cat) => (
            <div
              key={cat}
              className="rounded-xl overflow-hidden"
              style={{ background: "var(--color-surface)", boxShadow: "var(--shadow-raised)" }}
            >
              <div className="px-5 py-3 border-b border-border flex items-center gap-2">
                <ShoppingCart size={15} style={{ color: "var(--color-primary)" }} />
                <h3 className="text-sm font-semibold text-dark">{getCategoryLabel(cat)}</h3>
                <span
                  className="ml-auto text-xs font-medium px-2 py-0.5 rounded-full"
                  style={{ background: "var(--color-surface-down)", color: "var(--color-text-mid)" }}
                >
                  {grouped[cat].length}
                </span>
              </div>
              <table className="w-full text-sm">
                <tbody>
                  {grouped[cat].map((item, i) => (
                    <tr
                      key={item.ingredientId}
                      className="border-b border-border/40 last:border-none"
                      style={{ background: i % 2 === 0 ? "transparent" : "rgba(0,0,0,0.015)" }}
                    >
                      <td className="px-5 py-3 text-dark font-medium">{item.ingredientName}</td>
                      <td className="px-5 py-3 text-right data-value text-dark" style={{ fontFamily: "var(--font-mono)" }}>
                        {item.totalGrams.toFixed(0)}
                        <span className="text-text-mid ml-1 font-normal" style={{ fontFamily: "var(--font-body)" }}>g</span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ))}

          {/* Summary */}
          <div
            className="rounded-xl p-4 flex items-center justify-between"
            style={{ background: "var(--color-surface)", boxShadow: "var(--shadow-inset-sm)" }}
          >
            <span className="text-sm text-text-mid">{grocery.items.length} ingredients total</span>
            <span className="data-value text-sm font-bold text-dark" style={{ fontFamily: "var(--font-mono)" }}>
              {(grocery.items.reduce((s, i) => s + i.totalGrams, 0) / 1000).toFixed(2)} kg
            </span>
          </div>
        </div>
      )}

      <div className="flex justify-center mt-8">
        <Link
          to={`/analysis/${menuId}`}
          className="text-sm text-primary hover:underline"
        >
          ← View Nutrition Analysis
        </Link>
      </div>
    </div>
  );
}
