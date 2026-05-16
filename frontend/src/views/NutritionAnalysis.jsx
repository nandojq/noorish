import { useState } from "react";
import { useParams, useNavigate, Link } from "react-router-dom";
import { ArrowLeft, ChartBar, CalendarBlank } from "@phosphor-icons/react";
import { useMenuNutrition } from "@/hooks/useMenus";
import { useMenus } from "@/hooks/useMenus";
import { useSettings } from "@/hooks/useSettings";
import NutrientBars from "@/components/NutrientBars";
import { Skeleton } from "@/components/ui/skeleton";
import EmptyState from "@/components/EmptyState";

function formatDate(dateStr) {
  if (!dateStr) return "";
  const d = new Date(dateStr + "T00:00:00");
  return d.toLocaleDateString("en-GB", { weekday: "short", day: "numeric", month: "short" });
}

function CalorieGauge({ calories, target = 2000 }) {
  const pct = Math.min((calories / target) * 100, 120);
  const color = pct < 70 ? "var(--color-error)" : pct > 115 ? "var(--color-warning)" : "var(--color-success)";
  return (
    <div className="text-center">
      <p className="data-value text-2xl font-bold" style={{ color, fontFamily: "var(--font-mono)" }}>
        {Math.round(calories)}
      </p>
      <p className="text-xs text-text-mid">kcal</p>
      <div className="mt-2 h-1.5 rounded-full overflow-hidden" style={{ background: "var(--color-surface-down)" }}>
        <div className="h-full rounded-full transition-all" style={{ width: `${Math.min(pct, 100)}%`, background: color }} />
      </div>
      <p className="text-xs text-text-low mt-1">{Math.round(pct)}% of {target} target</p>
    </div>
  );
}

function DayCard({ day, onClick, isSelected }) {
  const cals = day.nutritionTotal?.calories || 0;
  return (
    <button
      onClick={onClick}
      className="text-left transition-all"
      style={{
        background: isSelected ? "var(--color-primary)" : "var(--color-surface)",
        borderRadius: "var(--radius-md)",
        boxShadow: isSelected ? "none" : "var(--shadow-raised-sm)",
        padding: "12px 16px",
        border: "none",
        cursor: "pointer",
        minWidth: 100,
      }}
    >
      <p className="text-xs font-semibold mb-1" style={{ color: isSelected ? "#fff" : "var(--color-text-mid)", letterSpacing: "0.06em", textTransform: "uppercase" }}>
        {formatDate(day.date)}
      </p>
      <p className="data-value text-base font-bold" style={{ fontFamily: "var(--font-mono)", color: isSelected ? "#fff" : "var(--color-text-high)" }}>
        {Math.round(cals)}
      </p>
      <p className="text-xs" style={{ color: isSelected ? "rgba(255,255,255,0.7)" : "var(--color-text-low)" }}>kcal</p>
    </button>
  );
}

export default function NutritionAnalysis() {
  const { menuId } = useParams();
  const navigate = useNavigate();
  const [selectedDay, setSelectedDay] = useState(null);

  const { data: menus } = useMenus();
  const { data: settings } = useSettings();
  const { data: nutrition, isLoading, error } = useMenuNutrition(menuId);

  const deficiencyThreshold = settings?.analysis?.deficiencyThresholdPercentDv ?? 70;
  const excessThreshold = settings?.analysis?.excessThresholdPercentDv ?? 150;

  const currentMenu = menus?.find((m) => m.id === menuId);

  // API only returns driComparison at the period level, not per day
  const driComparison = nutrition?.driComparison ?? [];

  if (isLoading) {
    return (
      <div className="max-w-5xl mx-auto p-6 space-y-6">
        <Skeleton className="h-8 w-64" />
        <Skeleton className="h-20 w-full" />
        <Skeleton className="h-96 w-full" />
      </div>
    );
  }

  if (error?.status === 422) {
    return (
      <div className="p-6">
        <EmptyState
          title="No nutrition data"
          description="Assign recipes to your menu to see the nutritional analysis."
          action={{ label: "Go to Menu Planner", onClick: () => navigate(`/menus/${menuId}`) }}
        />
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6 text-center">
        <p className="text-sm" style={{ color: "var(--color-error)" }}>Failed to load nutrition analysis.</p>
      </div>
    );
  }

  return (
    <div className="max-w-5xl mx-auto p-6">
      {/* Header */}
      <div className="flex items-center gap-4 mb-6">
        <button
          onClick={() => navigate(`/menus/${menuId}`)}
          className="icon-btn"
          aria-label="Back to menu"
        >
          <ArrowLeft size={18} />
        </button>
        <div className="flex-1">
          <h1 className="text-2xl font-bold text-dark" style={{ fontFamily: "var(--font-display)" }}>
            Nutrition Analysis
          </h1>
          {currentMenu && (
            <p className="text-sm text-text-mid mt-0.5">
              {currentMenu.name} · {currentMenu.startDate} → {currentMenu.endDate}
            </p>
          )}
        </div>
        {menus?.length > 1 && (
          <select
            value={menuId}
            onChange={(e) => navigate(`/analysis/${e.target.value}`)}
            className="h-9 rounded-lg border border-border bg-light text-sm text-dark px-3 focus:outline-none focus:ring-2 focus:ring-primary"
            style={{ boxShadow: "var(--shadow-inset-sm)" }}
          >
            {menus.map((m) => (
              <option key={m.id} value={m.id}>{m.name}</option>
            ))}
          </select>
        )}
      </div>

      {/* Period averages */}
      {nutrition?.dailyAverage && (
        <div
          className="rounded-xl mb-6 p-5"
          style={{ background: "var(--color-surface)", boxShadow: "var(--shadow-raised)" }}
        >
          <div className="flex items-center gap-2 mb-4">
            <ChartBar size={18} style={{ color: "var(--color-primary)" }} />
            <h2 className="font-semibold text-dark" style={{ fontFamily: "var(--font-display)", fontSize: "1.05rem" }}>
              Weekly Average
            </h2>
          </div>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-4">
            {[
              { label: "Calories", value: Math.round(nutrition.dailyAverage.calories || 0), unit: "kcal" },
              { label: "Protein", value: (nutrition.dailyAverage.macronutrients?.protein || 0).toFixed(1), unit: "g" },
              { label: "Carbs", value: (nutrition.dailyAverage.macronutrients?.carbohydrates || 0).toFixed(1), unit: "g" },
              { label: "Fat", value: (nutrition.dailyAverage.macronutrients?.fat || 0).toFixed(1), unit: "g" },
            ].map(({ label, value, unit }) => (
              <div
                key={label}
                className="text-center py-3 rounded-lg"
                style={{ background: "var(--color-surface)", boxShadow: "var(--shadow-inset-sm)" }}
              >
                <p className="data-value text-xl font-bold text-dark" style={{ fontFamily: "var(--font-mono)" }}>
                  {value}
                  <span className="text-xs text-text-mid ml-1">{unit}</span>
                </p>
                <p className="text-xs text-text-mid mt-0.5">{label}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Day-by-day cards */}
      {nutrition?.days?.length > 0 && (
        <div
          className="rounded-xl mb-6 p-5"
          style={{ background: "var(--color-surface)", boxShadow: "var(--shadow-raised)" }}
        >
          <div className="flex items-center gap-2 mb-4">
            <CalendarBlank size={18} style={{ color: "var(--color-secondary)" }} />
            <h2 className="font-semibold text-dark" style={{ fontFamily: "var(--font-display)", fontSize: "1.05rem" }}>
              Day by Day
            </h2>
            {selectedDay != null && (
              <button
                onClick={() => setSelectedDay(null)}
                className="ml-auto text-xs text-text-mid hover:text-primary underline"
              >
                Show all days
              </button>
            )}
          </div>
          <div className="flex gap-3 overflow-x-auto pb-2">
            {nutrition.days.map((day, i) => (
              <DayCard
                key={day.date}
                day={day}
                isSelected={selectedDay === i}
                onClick={() => setSelectedDay(selectedDay === i ? null : i)}
              />
            ))}
          </div>
        </div>
      )}

      {/* Nutrient chart */}
      <div
        className="rounded-xl p-5"
        style={{ background: "var(--color-surface)", boxShadow: "var(--shadow-raised)" }}
      >
        <h2 className="font-semibold text-dark mb-1" style={{ fontFamily: "var(--font-display)", fontSize: "1.05rem" }}>
          Nutrients — Weekly Average
        </h2>
        <p className="text-xs text-text-mid mb-5">
          Bars show % of Daily Value achieved.
          <span className="mx-2 text-text-low">·</span>
          <span style={{ color: "var(--color-error)" }}>Below {deficiencyThreshold}% = deficient</span>
          <span className="mx-2 text-text-low">·</span>
          <span style={{ color: "var(--color-warning)" }}>Above {excessThreshold}% = excess</span>
        </p>

        <NutrientBars
          driComparison={driComparison}
          deficiencyThreshold={deficiencyThreshold}
          excessThreshold={excessThreshold}
        />
      </div>

      <div className="flex justify-center mt-8">
        <Link
          to={`/grocery/${menuId}`}
          className="btn-primary"
          style={{ textDecoration: "none" }}
        >
          View Grocery List →
        </Link>
      </div>
    </div>
  );
}
