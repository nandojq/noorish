import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  Cell,
  ReferenceLine,
  ResponsiveContainer,
} from "recharts";

/* Recharts fill props require literal color values, not CSS variables */
const DEFICIENT_COLOR = "#C93434";  /* kf error red */
const ADEQUATE_COLOR  = "#12A99A";  /* kf-teal-400 */
const EXCESS_COLOR    = "#E06620";  /* kf-orange-400 */
const AXIS_COLOR      = "#161A1F";  /* kf-neutral-900 */

function getColor(percentDv, deficiencyThreshold, excessThreshold) {
  if (percentDv < deficiencyThreshold) return DEFICIENT_COLOR;
  if (percentDv > excessThreshold) return EXCESS_COLOR;
  return ADEQUATE_COLOR;
}

function formatNutrientName(name) {
  return name
    .replace(/_/g, " ")
    .replace(/\b\w/g, (c) => c.toUpperCase());
}

function CustomTooltip({ active, payload }) {
  if (!active || !payload?.length) return null;
  const d = payload[0]?.payload;
  if (!d) return null;
  return (
    <div className="bg-kf-blue-900 text-kf-blue-50 rounded-lg px-3 py-2 text-xs popover-shadow">
      <p className="font-semibold">{formatNutrientName(d.nutrient)}</p>
      <p>
        {d.dailyAverageValue?.toFixed(1)} {d.unit}
      </p>
      <p>{d.percentDv?.toFixed(1)}% DV</p>
    </div>
  );
}

export default function NutrientBars({
  driComparison = [],
  deficiencyThreshold = 70,
  excessThreshold = 150,
}) {
  const data = driComparison.map((item) => ({
    ...item,
    barValue: Math.min(item.percentDv, 200) / 2,
  }));

  if (!data.length) {
    return (
      <p className="text-sm text-text-mid text-center py-8">No nutrient data available.</p>
    );
  }

  const defLine = deficiencyThreshold / 2;
  const excLine = Math.min(excessThreshold, 200) / 2;

  return (
    <ResponsiveContainer width="100%" height={data.length * 32 + 40}>
      <BarChart
        layout="vertical"
        data={data}
        margin={{ top: 8, right: 48, left: 140, bottom: 8 }}
      >
        <XAxis
          type="number"
          domain={[0, 100]}
          tickFormatter={(v) => `${v * 2}%`}
          tick={{ fontSize: 10, fill: AXIS_COLOR }}
        />
        <YAxis
          type="category"
          dataKey="nutrient"
          tickFormatter={formatNutrientName}
          tick={{ fontSize: 11, fill: AXIS_COLOR }}
          width={136}
        />
        <Tooltip content={<CustomTooltip />} />
        <ReferenceLine
          x={50}
          stroke={AXIS_COLOR}
          strokeDasharray="2 2"
          label={{ value: "100%", position: "right", fontSize: 10, fill: AXIS_COLOR }}
        />
        <ReferenceLine
          x={defLine}
          stroke={DEFICIENT_COLOR}
          strokeDasharray="4 2"
          label={{ value: `${deficiencyThreshold}%`, position: "right", fontSize: 10, fill: DEFICIENT_COLOR }}
        />
        {excessThreshold <= 200 && (
          <ReferenceLine
            x={excLine}
            stroke={EXCESS_COLOR}
            strokeDasharray="4 2"
            label={{ value: `${excessThreshold}%`, position: "right", fontSize: 10, fill: EXCESS_COLOR }}
          />
        )}
        <Bar dataKey="barValue" radius={[0, 3, 3, 0]}>
          {data.map((entry, index) => (
            <Cell
              key={index}
              fill={getColor(entry.percentDv, deficiencyThreshold, excessThreshold)}
            />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  );
}
