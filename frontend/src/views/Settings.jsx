import { useState, useEffect } from "react";
import { toast } from "sonner";
import { FloppyDisk } from "@phosphor-icons/react";
import { useSettings, useUpdateSettings } from "@/hooks/useSettings";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";

function FieldGroup({ label, description, children }) {
  return (
    <div className="flex items-start justify-between gap-6 py-5 border-b border-border last:border-none">
      <div className="flex-1">
        <p className="text-sm font-semibold text-text-high">{label}</p>
        {description && <p className="text-xs text-text-high mt-0.5">{description}</p>}
      </div>
      <div className="shrink-0">{children}</div>
    </div>
  );
}

function NeuInput({ value, onChange, min, max, error }) {
  return (
    <div>
      <div className="relative">
        <input
          type="number"
          value={value}
          onChange={onChange}
          min={min}
          max={max}
          className="w-24 text-center font-mono text-text-high text-sm rounded-lg border border-border bg-surface-alt h-9 px-3 focus:outline-none focus:ring-2 focus:ring-primary"
          style={{ boxShadow: "var(--shadow-inset-sm)" }}
        />
        <span className="absolute right-2 top-1/2 -translate-y-1/2 text-xs text-text-low pointer-events-none">%</span>
      </div>
      {error && <p className="text-xs text-error mt-1">{error}</p>}
    </div>
  );
}

export default function Settings() {
  const { data: settings, isLoading } = useSettings();
  const updateSettings = useUpdateSettings();

  const [deficiency, setDeficiency] = useState("");
  const [excess, setExcess] = useState("");
  const [errors, setErrors] = useState({});

  useEffect(() => {
    if (settings?.analysis) {
      setDeficiency(String(settings.analysis.deficiencyThresholdPercentDv ?? 70));
      setExcess(String(settings.analysis.excessThresholdPercentDv ?? 150));
    }
  }, [settings]);

  const validate = () => {
    const d = Number(deficiency);
    const e = Number(excess);
    const errs = {};
    if (isNaN(d) || d < 1 || d >= 100) errs.deficiency = "Must be between 1 and 99";
    if (isNaN(e) || e <= 100) errs.excess = "Must be greater than 100";
    if (!errs.deficiency && !errs.excess && d >= e) errs.excess = "Must be greater than deficiency threshold";
    setErrors(errs);
    return Object.keys(errs).length === 0;
  };

  const handleSave = () => {
    if (!validate()) return;
    updateSettings.mutate(
      {
        analysis: {
          deficiencyThresholdPercentDv: Number(deficiency),
          excessThresholdPercentDv: Number(excess),
        },
      },
      {
        onSuccess: () => toast.success("Settings saved"),
        onError: (err) => toast.error(err.message || "Failed to save settings"),
      }
    );
  };

  return (
    <div className="max-w-2xl mx-auto p-6">
      <h1 className="text-2xl font-bold text-text-high mb-1" style={{ fontFamily: "var(--font-display)" }}>
        Settings
      </h1>
      <p className="text-sm text-text-high mb-8">Configure analysis thresholds and preferences.</p>

      {/* Nutrition Thresholds */}
      <div
        className="rounded-xl overflow-hidden mb-6 border border-border"
        style={{ background: "var(--color-surface)" }}
      >
        <div className="px-6 py-4 border-b border-border">
          <h2 className="font-semibold text-text-high" style={{ fontFamily: "var(--font-display)", fontSize: "1.05rem" }}>
            Nutrition Thresholds
          </h2>
          <p className="text-xs text-text-high mt-0.5">
            Controls how nutrients are flagged in the analysis view. Based on % of Daily Value (DV).
          </p>
        </div>

        <div className="px-6">
          {isLoading ? (
            <div className="space-y-4 py-4">
              <Skeleton className="h-10 w-full" />
              <Skeleton className="h-10 w-full" />
            </div>
          ) : (
            <>
              <FieldGroup
                label="Deficiency threshold"
                description="Nutrients below this % DV are flagged as deficient (red). Default: 70%."
              >
                <NeuInput
                  value={deficiency}
                  onChange={(e) => setDeficiency(e.target.value)}
                  min={1}
                  max={99}
                  error={errors.deficiency}
                />
              </FieldGroup>

              <FieldGroup
                label="Excess threshold"
                description="Nutrients above this % DV are flagged as excess (amber). Default: 150%."
              >
                <NeuInput
                  value={excess}
                  onChange={(e) => setExcess(e.target.value)}
                  min={101}
                  error={errors.excess}
                />
              </FieldGroup>
            </>
          )}
        </div>
      </div>

      {/* Threshold visual guide */}
      <div
        className="rounded-xl border border-border p-4 mb-8"
        style={{ background: "var(--color-surface)" }}
      >
        <p className="text-xs font-medium text-text-high mb-3 uppercase tracking-wide">Colour coding guide</p>
        <div className="flex flex-col gap-2">
          {[
            { color: "var(--color-error)", label: `Below ${deficiency || "70"}% DV`, desc: "Deficient" },
            { color: "var(--color-success)", label: `${deficiency || "70"}% – ${excess || "150"}% DV`, desc: "Adequate" },
            { color: "var(--color-warning)", label: `Above ${excess || "150"}% DV`, desc: "Excess" },
          ].map(({ color, label, desc }) => (
            <div key={desc} className="flex items-center gap-3">
              <div className="w-3 h-3 rounded-full shrink-0" style={{ background: color }} />
              <span className="text-xs font-medium text-text-high w-40">{label}</span>
              <span className="text-xs text-text-mid">{desc}</span>
            </div>
          ))}
        </div>
      </div>

      <div className="flex justify-end">
        <button
          onClick={handleSave}
          disabled={updateSettings.isPending}
          className="btn-primary flex items-center gap-2 disabled:opacity-50"
        >
          <FloppyDisk size={16} weight="regular" />
          {updateSettings.isPending ? "Saving…" : "Save Settings"}
        </button>
      </div>

      {/* Data Sources placeholder */}
      <div
        className="rounded-xl overflow-hidden mt-8 border border-border"
        style={{ background: "var(--color-surface)" }}
      >
        <div className="px-6 py-4 border-b border-border">
          <h2 className="font-semibold text-text-high" style={{ fontFamily: "var(--font-display)", fontSize: "1.05rem" }}>
            Data Sources
          </h2>
          <p className="text-xs text-text-high mt-0.5">Phase 2 — Coming soon.</p>
        </div>
        <div className="px-6 py-4 text-sm text-text-high">
          USDA FoodData Central and Open Food Facts integration toggles will appear here.
        </div>
      </div>
    </div>
  );
}
