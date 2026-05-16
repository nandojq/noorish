# 🌿 NutriWell — Frontend Design System & Styling Guide

> A warm, neumorphic nutrition web application for health-conscious adults.  
> Inspired by the iridescent plumage of the **European Kingfisher** (*Alcedo atthis*).

---

## 1. Design Philosophy

This app is built on three pillars:

- **Warmth** — users are on a health journey; the interface should feel like a knowledgeable, encouraging companion, never clinical or cold.
- **Clarity** — nutrition data can be complex. The UI strips away noise and presents information with generous breathing room and clear hierarchy.
- **Softness** — neumorphism creates a tactile, almost physical feel. Cards feel pressable. Inputs feel recessed. Everything has weight and depth.

---

## 2. Color Palette — The Kingfisher

The European Kingfisher is one of nature's most stunning birds: deep cobalt blue on the back, vivid electric turquoise on the crown, and a striking warm orange-amber on the breast. We translate this into soft pastels for a welcoming, modern feel.

### 2.1 Core Palette

| Role | Name | Hex | Usage |
|---|---|---|---|
| Background | Soft Cloud | `#F0F4F5` | Page background, base surface |
| Surface | Pearl Mist | `#E8EEF0` | Cards, panels, containers |
| Primary | Kingfisher Blue | `#7FB5C8` | Primary buttons, active states, links |
| Secondary | Teal Crown | `#6ECFC0` | Accents, tags, highlights |
| Accent | Amber Breast | `#E8A87C` | CTAs, warnings, focus rings, badges |
| Accent Light | Peach Glow | `#F5C9A8` | Hover states, soft highlights |
| Text Dark | Deep Slate | `#2E3D42` | Headings, primary text |
| Text Mid | Storm Blue | `#5A7A85` | Body text, secondary labels |
| Text Light | Pale Haze | `#9BB4BC` | Placeholders, disabled states, captions |
| Success | Sage Reed | `#89C4A0` | Positive feedback, healthy indicators |
| Warning | Amber Wing | `#E8A87C` | Caution, near-limit indicators |
| Error | Coral Dusk | `#E07C7C` | Errors, over-limit alerts |

### 2.2 CSS Custom Properties

```css
:root {
  /* Base surfaces */
  --color-bg:           #F0F4F5;
  --color-surface:      #E8EEF0;
  --color-surface-up:   #F5F8F9;   /* raised elements */
  --color-surface-down: #D8E2E6;   /* pressed / inset elements */

  /* Brand */
  --color-primary:      #7FB5C8;
  --color-primary-dark: #5A9AB5;
  --color-secondary:    #6ECFC0;
  --color-accent:       #E8A87C;
  --color-accent-light: #F5C9A8;

  /* Text */
  --color-text-high:    #2E3D42;
  --color-text-mid:     #5A7A85;
  --color-text-low:     #9BB4BC;

  /* Semantic */
  --color-success:      #89C4A0;
  --color-warning:      #E8A87C;
  --color-error:        #E07C7C;

  /* Neumorphic shadows — the heart of the style */
  --shadow-raised:
    6px 6px 14px #C8D4D8,
   -6px -6px 14px #FFFFFF;

  --shadow-raised-sm:
    3px 3px 8px #C8D4D8,
   -3px -3px 8px #FFFFFF;

  --shadow-inset:
    inset 4px 4px 10px #C8D4D8,
    inset -4px -4px 10px #FFFFFF;

  --shadow-inset-sm:
    inset 2px 2px 6px #C8D4D8,
    inset -2px -2px 6px #FFFFFF;

  --shadow-pressed:
    inset 3px 3px 8px #B8C8CE,
    inset -3px -3px 8px #FFFFFF;

  /* Spacing scale */
  --space-xs:   4px;
  --space-sm:   8px;
  --space-md:   16px;
  --space-lg:   24px;
  --space-xl:   40px;
  --space-2xl:  64px;

  /* Border radius */
  --radius-sm:  8px;
  --radius-md:  14px;
  --radius-lg:  20px;
  --radius-xl:  28px;
  --radius-pill: 999px;

  /* Transitions */
  --transition-fast:   150ms ease;
  --transition-base:   250ms ease;
  --transition-slow:   400ms ease;
}
```

---

## 3. Typography

Pair a distinctive humanist display font with a refined, legible body font. The combination should feel warm and approachable — never sterile.

### 3.1 Font Stack

| Role | Font | Source | Weight |
|---|---|---|---|
| Display / Headings | **Lora** | Google Fonts | 500, 600, 700 |
| Body / UI | **DM Sans** | Google Fonts | 300, 400, 500 |
| Data / Numbers | **DM Mono** | Google Fonts | 400, 500 |

```html
<!-- In your <head> -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Lora:wght@500;600;700&family=DM+Sans:wght@300;400;500&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">
```

### 3.2 Type Scale

```css
:root {
  --font-display: 'Lora', Georgia, serif;
  --font-body:    'DM Sans', system-ui, sans-serif;
  --font-mono:    'DM Mono', monospace;

  --text-xs:   0.75rem;    /* 12px — captions, badges */
  --text-sm:   0.875rem;   /* 14px — labels, helper text */
  --text-base: 1rem;       /* 16px — body copy */
  --text-lg:   1.125rem;   /* 18px — lead text */
  --text-xl:   1.375rem;   /* 22px — card headings */
  --text-2xl:  1.75rem;    /* 28px — section titles */
  --text-3xl:  2.25rem;    /* 36px — page headings */
  --text-4xl:  3rem;       /* 48px — hero display */

  --leading-tight:  1.2;
  --leading-normal: 1.5;
  --leading-loose:  1.8;
}

/* Base styles */
body {
  font-family: var(--font-body);
  font-size: var(--text-base);
  line-height: var(--leading-normal);
  color: var(--color-text-high);
  background-color: var(--color-bg);
  -webkit-font-smoothing: antialiased;
}

h1, h2, h3 {
  font-family: var(--font-display);
  line-height: var(--leading-tight);
  color: var(--color-text-high);
}

h4, h5, h6, label, button {
  font-family: var(--font-body);
  font-weight: 500;
}

/* Numeric data — macros, calories, grams */
.data-value {
  font-family: var(--font-mono);
  font-weight: 500;
  letter-spacing: -0.02em;
}
```

---

## 4. Neumorphism — The Core Style System

Neumorphism works by casting two shadows from every element: one dark (bottom-right, simulating a light source from top-left) and one white (top-left highlight). The background and element colors **must match** for the illusion to hold.

### 4.1 The Golden Rules

1. **Background = Surface color.** Elements must share the same base color as the background. Never place neumorphic cards on a contrasting background.
2. **Subtle, not harsh.** Shadow opacity should stay between 30–50%. Stronger shadows look broken.
3. **Use sparingly.** Not every element needs neumorphism. Reserve it for cards, inputs, and key interactive elements.
4. **Flat for interactive states.** When pressed/active, switch to inset shadows to simulate a physical press.
5. **Accessible contrast.** Because backgrounds and surfaces are close in value, always ensure text meets WCAG AA contrast (4.5:1 minimum).

### 4.2 Elevation Levels

```css
/* Level 0 — Flat (no elevation) */
.neu-flat {
  background: var(--color-surface);
}

/* Level 1 — Raised card (default resting state) */
.neu-raised {
  background: var(--color-surface);
  box-shadow: var(--shadow-raised);
  border-radius: var(--radius-md);
}

/* Level 2 — Elevated (hover state) */
.neu-elevated {
  background: var(--color-surface-up);
  box-shadow:
    10px 10px 20px #C0CCCE,
    -10px -10px 20px #FFFFFF;
  border-radius: var(--radius-md);
}

/* Level 3 — Inset (inputs, recessed containers, pressed) */
.neu-inset {
  background: var(--color-surface);
  box-shadow: var(--shadow-inset);
  border-radius: var(--radius-md);
}
```

---

## 5. Component Library

### 5.1 Cards

The primary container unit. Used for meal cards, nutrient panels, weekly summaries.

```css
.card {
  background: var(--color-surface);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-raised);
  padding: var(--space-lg);
  transition: box-shadow var(--transition-base), transform var(--transition-base);
}

.card:hover {
  box-shadow:
    10px 10px 22px #BFCDD2,
    -10px -10px 22px #FFFFFF;
  transform: translateY(-2px);
}

/* Compact variant for dense grids */
.card--sm {
  border-radius: var(--radius-md);
  padding: var(--space-md);
}

/* Inset variant for inner sections */
.card--inset {
  box-shadow: var(--shadow-inset);
}
```

### 5.2 Buttons

```css
/* Primary Button */
.btn-primary {
  font-family: var(--font-body);
  font-weight: 500;
  font-size: var(--text-sm);
  letter-spacing: 0.03em;
  color: #FFFFFF;
  background: linear-gradient(135deg, var(--color-primary), var(--color-primary-dark));
  border: none;
  border-radius: var(--radius-pill);
  padding: 12px 28px;
  box-shadow:
    4px 4px 10px rgba(95, 154, 181, 0.4),
    -2px -2px 8px rgba(255, 255, 255, 0.6);
  cursor: pointer;
  transition: all var(--transition-base);
}

.btn-primary:hover {
  box-shadow:
    6px 6px 14px rgba(95, 154, 181, 0.5),
    -3px -3px 10px rgba(255, 255, 255, 0.7);
  transform: translateY(-1px);
}

.btn-primary:active {
  box-shadow:
    inset 3px 3px 8px rgba(60, 110, 140, 0.4),
    inset -2px -2px 6px rgba(255, 255, 255, 0.4);
  transform: translateY(0);
}

/* Secondary Button */
.btn-secondary {
  font-family: var(--font-body);
  font-weight: 500;
  font-size: var(--text-sm);
  color: var(--color-primary-dark);
  background: var(--color-surface);
  border: none;
  border-radius: var(--radius-pill);
  padding: 12px 28px;
  box-shadow: var(--shadow-raised-sm);
  cursor: pointer;
  transition: all var(--transition-base);
}

.btn-secondary:hover {
  box-shadow: var(--shadow-raised);
  color: var(--color-primary);
}

.btn-secondary:active {
  box-shadow: var(--shadow-pressed);
}

/* Accent / CTA Button */
.btn-accent {
  background: linear-gradient(135deg, var(--color-accent), #D4906A);
  color: #FFFFFF;
  /* Same structure as btn-primary */
}
```

### 5.3 Inputs & Form Fields

```css
.input-field {
  width: 100%;
  font-family: var(--font-body);
  font-size: var(--text-base);
  color: var(--color-text-high);
  background: var(--color-surface);
  border: none;
  border-radius: var(--radius-md);
  padding: 14px 18px;
  box-shadow: var(--shadow-inset);
  outline: none;
  transition: box-shadow var(--transition-base);
}

.input-field::placeholder {
  color: var(--color-text-low);
}

.input-field:focus {
  box-shadow:
    var(--shadow-inset),
    0 0 0 2px var(--color-primary);
}

.input-label {
  font-size: var(--text-sm);
  font-weight: 500;
  color: var(--color-text-mid);
  margin-bottom: var(--space-xs);
  display: block;
}

/* Select dropdown */
.select-field {
  appearance: none;
  background-image: url("data:image/svg+xml,..."); /* custom arrow */
  background-repeat: no-repeat;
  background-position: right 14px center;
  padding-right: 42px;
  /* inherits .input-field styles */
}
```

### 5.4 Nutrient Progress Bars

The key UI element for this app. Shows macro/micronutrient progress against daily targets.

```css
.nutrient-track {
  display: flex;
  flex-direction: column;
  gap: var(--space-xs);
}

.nutrient-track__header {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
}

.nutrient-track__label {
  font-size: var(--text-sm);
  font-weight: 500;
  color: var(--color-text-mid);
}

.nutrient-track__value {
  font-family: var(--font-mono);
  font-size: var(--text-sm);
  color: var(--color-text-high);
}

/* The bar container */
.nutrient-bar {
  height: 10px;
  border-radius: var(--radius-pill);
  background: var(--color-surface);
  box-shadow: var(--shadow-inset-sm);
  overflow: hidden;
}

/* The fill */
.nutrient-bar__fill {
  height: 100%;
  border-radius: var(--radius-pill);
  transition: width var(--transition-slow);
}

/* Variants by nutrient type */
.nutrient-bar__fill--protein  { background: linear-gradient(90deg, #7FB5C8, #6ECFC0); }
.nutrient-bar__fill--carbs    { background: linear-gradient(90deg, #E8A87C, #F5C9A8); }
.nutrient-bar__fill--fat      { background: linear-gradient(90deg, #89C4A0, #6ECFC0); }
.nutrient-bar__fill--calories { background: linear-gradient(90deg, #7FB5C8, var(--color-accent)); }

/* Warning state — approaching limit */
.nutrient-bar__fill--warning  { background: linear-gradient(90deg, #E8A87C, #E07C7C); }

/* Over limit */
.nutrient-bar__fill--over     { background: linear-gradient(90deg, #E07C7C, #C05050); }
```

### 5.5 Macro Summary Ring (SVG)

Use an SVG donut chart for the daily macro breakdown — protein, carbs, fat.

```jsx
// React example
const MacroRing = ({ protein, carbs, fat }) => {
  const total = protein + carbs + fat;
  const r = 54;
  const circumference = 2 * Math.PI * r;

  const proteinDash = (protein / total) * circumference;
  const carbsDash   = (carbs / total) * circumference;
  const fatDash     = (fat / total) * circumference;

  return (
    <svg viewBox="0 0 120 120" width="120" height="120">
      {/* Background track */}
      <circle cx="60" cy="60" r={r} fill="none"
        stroke="#D8E2E6" strokeWidth="12" />

      {/* Protein segment */}
      <circle cx="60" cy="60" r={r} fill="none"
        stroke="#7FB5C8" strokeWidth="12"
        strokeDasharray={`${proteinDash} ${circumference}`}
        strokeLinecap="round"
        transform="rotate(-90 60 60)" />

      {/* Carbs segment */}
      <circle cx="60" cy="60" r={r} fill="none"
        stroke="#E8A87C" strokeWidth="12"
        strokeDasharray={`${carbsDash} ${circumference}`}
        strokeDashoffset={-proteinDash}
        transform="rotate(-90 60 60)" />

      {/* Fat segment */}
      <circle cx="60" cy="60" r={r} fill="none"
        stroke="#89C4A0" strokeWidth="12"
        strokeDasharray={`${fatDash} ${circumference}`}
        strokeDashoffset={-(proteinDash + carbsDash)}
        transform="rotate(-90 60 60)" />

      {/* Center label */}
      <text x="60" y="56" textAnchor="middle"
        fontSize="18" fontWeight="600" fill="#2E3D42"
        fontFamily="DM Mono">{total}g</text>
      <text x="60" y="70" textAnchor="middle"
        fontSize="9" fill="#9BB4BC"
        fontFamily="DM Sans">total macros</text>
    </svg>
  );
};
```

### 5.6 Meal Tags / Badges

```css
.tag {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: var(--text-xs);
  font-weight: 500;
  padding: 4px 12px;
  border-radius: var(--radius-pill);
  box-shadow: var(--shadow-raised-sm);
}

.tag--protein  { color: var(--color-primary-dark); background: #D6EAF2; }
.tag--vegan    { color: #3A8A60; background: #D4EDE0; }
.tag--highcal  { color: #9A5030; background: #FAE2D0; }
.tag--lowcarb  { color: #5A7A85; background: #D6EBE8; }
```

---

## 6. Layout System

### 6.1 Grid & Spacing

```css
/* Page wrapper */
.page-wrapper {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 var(--space-xl);
}

/* Main layout — sidebar + content */
.app-layout {
  display: grid;
  grid-template-columns: 260px 1fr;
  grid-template-rows: 64px 1fr;
  grid-template-areas:
    "sidebar topbar"
    "sidebar main";
  min-height: 100vh;
  gap: 0;
}

/* Weekly meal planner grid — 7 columns */
.meal-week-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: var(--space-md);
}

/* Responsive — collapse to 2 columns on tablet */
@media (max-width: 900px) {
  .meal-week-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  .app-layout {
    grid-template-columns: 1fr;
    grid-template-areas:
      "topbar"
      "main";
  }
}
```

### 6.2 Sidebar Navigation

```css
.sidebar {
  grid-area: sidebar;
  background: var(--color-surface);
  box-shadow:
    6px 0 20px rgba(0, 0, 0, 0.06);
  padding: var(--space-xl) var(--space-lg);
  display: flex;
  flex-direction: column;
  gap: var(--space-sm);
}

.nav-item {
  display: flex;
  align-items: center;
  gap: var(--space-md);
  padding: 12px var(--space-md);
  border-radius: var(--radius-md);
  font-weight: 500;
  font-size: var(--text-sm);
  color: var(--color-text-mid);
  text-decoration: none;
  transition: all var(--transition-base);
  cursor: pointer;
}

.nav-item:hover {
  background: var(--color-surface);
  box-shadow: var(--shadow-raised-sm);
  color: var(--color-primary);
}

.nav-item--active {
  background: var(--color-surface);
  box-shadow: var(--shadow-raised);
  color: var(--color-primary-dark);
}

.nav-item__icon {
  width: 20px;
  height: 20px;
  color: inherit;
}
```

### 6.3 Top Bar

```css
.topbar {
  grid-area: topbar;
  background: var(--color-bg);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 var(--space-xl);
  box-shadow: 0 2px 12px rgba(0,0,0,0.04);
}

.topbar__title {
  font-family: var(--font-display);
  font-size: var(--text-xl);
  color: var(--color-text-high);
}

.topbar__actions {
  display: flex;
  align-items: center;
  gap: var(--space-md);
}
```

---

## 7. Weekly Meal Planner — Key Screen

### 7.1 Day Column Card

```css
.day-column {
  background: var(--color-surface);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-raised);
  padding: var(--space-md);
  display: flex;
  flex-direction: column;
  gap: var(--space-sm);
  min-height: 400px;
}

.day-column__header {
  font-family: var(--font-display);
  font-size: var(--text-sm);
  font-weight: 600;
  color: var(--color-text-mid);
  text-transform: uppercase;
  letter-spacing: 0.08em;
  padding-bottom: var(--space-sm);
  border-bottom: 1px solid var(--color-surface-down);
}

.day-column__header--today {
  color: var(--color-primary);
}
```

### 7.2 Meal Slot Card

```css
.meal-slot {
  background: var(--color-surface);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-raised-sm);
  padding: var(--space-sm) var(--space-md);
  cursor: pointer;
  transition: all var(--transition-base);
}

.meal-slot:hover {
  box-shadow: var(--shadow-raised);
  transform: translateY(-1px);
}

.meal-slot--empty {
  box-shadow: var(--shadow-inset-sm);
  border: 2px dashed var(--color-text-low);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-text-low);
  font-size: var(--text-sm);
  min-height: 56px;
}

.meal-slot__name {
  font-size: var(--text-sm);
  font-weight: 500;
  color: var(--color-text-high);
}

.meal-slot__cals {
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  color: var(--color-text-mid);
}
```

---

## 8. Iconography

Use **Phosphor Icons** — they have a warm, slightly rounded style that fits neumorphism perfectly.

```html
<script src="https://unpkg.com/@phosphor-icons/web"></script>
<!-- Usage -->
<i class="ph ph-bowl-food"></i>
<i class="ph ph-carrot"></i>
<i class="ph ph-chart-pie"></i>
<i class="ph ph-calendar-blank"></i>
<i class="ph ph-drop"></i>
<i class="ph ph-fire"></i>
```

```css
/* Icon sizing */
.icon-sm  { font-size: 16px; }
.icon-md  { font-size: 20px; }
.icon-lg  { font-size: 24px; }
.icon-xl  { font-size: 32px; }

/* Icon in neumorphic button/circle */
.icon-btn {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: var(--color-surface);
  box-shadow: var(--shadow-raised-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all var(--transition-base);
  border: none;
}

.icon-btn:hover  { box-shadow: var(--shadow-raised); }
.icon-btn:active { box-shadow: var(--shadow-pressed); }
```

---

## 9. Micro-interactions & Motion

Keep animations purposeful and gentle — this is a calm, nurturing app.

```css
/* Page section fade-in on load */
@keyframes fadeSlideUp {
  from {
    opacity: 0;
    transform: translateY(16px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-in {
  animation: fadeSlideUp 0.4s ease forwards;
}

/* Stagger children */
.card:nth-child(1) { animation-delay: 0ms;  }
.card:nth-child(2) { animation-delay: 60ms; }
.card:nth-child(3) { animation-delay: 120ms;}
.card:nth-child(4) { animation-delay: 180ms;}

/* Progress bar fill animation */
.nutrient-bar__fill {
  animation: fillBar 0.8s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
}

@keyframes fillBar {
  from { width: 0%; }
}

/* Pulse for loading states */
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50%       { opacity: 0.5; }
}

.skeleton {
  background: var(--color-surface-down);
  border-radius: var(--radius-sm);
  animation: pulse 1.6s ease infinite;
}
```

---

## 10. Accessibility & Dark Mode

### 10.1 Accessibility

```css
/* Focus visible — always override, never remove */
:focus-visible {
  outline: 2px solid var(--color-accent);
  outline-offset: 3px;
  border-radius: var(--radius-sm);
}

/* Reduced motion */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}

/* Minimum touch target */
button, a, [role="button"] {
  min-height: 44px;
  min-width: 44px;
}
```

### 10.2 Dark Mode

Neumorphism adapts gracefully to dark mode — same principle, darker base.

```css
@media (prefers-color-scheme: dark) {
  :root {
    --color-bg:           #1E2A2E;
    --color-surface:      #243036;
    --color-surface-up:   #2C3A40;
    --color-surface-down: #18232A;

    --color-text-high:    #E8F0F3;
    --color-text-mid:     #9BBAC4;
    --color-text-low:     #5A7A85;

    --shadow-raised:
       6px  6px 14px #141E22,
      -6px -6px 14px #2E3E46;

    --shadow-inset:
      inset  4px  4px 10px #141E22,
      inset -4px -4px 10px #2E3E46;
  }
}
```

---

## 11. Do's and Don'ts

### ✅ Do
- Always pair neumorphic shadows with the **exact same background color** as the surface
- Use **Lora** for any display text, macro totals, or section headings
- Keep interactive states distinct: raised → hover elevated → active pressed
- Use the **amber accent** (`#E8A87C`) sparingly — reserve it for the most important actions
- Test every card/button on the exact background color it sits on

### ❌ Don't
- Don't place neumorphic elements on white or strongly contrasting backgrounds
- Don't use more than 3 font weights in one view
- Don't make shadows too dark — they should whisper, not shout
- Don't use pure black (`#000000`) anywhere — use `--color-text-high` instead
- Don't over-animate — one transition per interaction is enough

---

## 12. Quick Reference — Copy-Paste Tokens

```css
/* Paste this block at the top of your main CSS file */

:root {
  --color-bg: #F0F4F5; --color-surface: #E8EEF0;
  --color-surface-up: #F5F8F9; --color-surface-down: #D8E2E6;
  --color-primary: #7FB5C8; --color-primary-dark: #5A9AB5;
  --color-secondary: #6ECFC0; --color-accent: #E8A87C;
  --color-accent-light: #F5C9A8;
  --color-text-high: #2E3D42; --color-text-mid: #5A7A85;
  --color-text-low: #9BB4BC;
  --color-success: #89C4A0; --color-warning: #E8A87C;
  --color-error: #E07C7C;
  --shadow-raised: 6px 6px 14px #C8D4D8, -6px -6px 14px #FFFFFF;
  --shadow-raised-sm: 3px 3px 8px #C8D4D8, -3px -3px 8px #FFFFFF;
  --shadow-inset: inset 4px 4px 10px #C8D4D8, inset -4px -4px 10px #FFFFFF;
  --shadow-inset-sm: inset 2px 2px 6px #C8D4D8, inset -2px -2px 6px #FFFFFF;
  --shadow-pressed: inset 3px 3px 8px #B8C8CE, inset -3px -3px 8px #FFFFFF;
  --radius-sm: 8px; --radius-md: 14px; --radius-lg: 20px;
  --radius-xl: 28px; --radius-pill: 999px;
  --font-display: 'Lora', Georgia, serif;
  --font-body: 'DM Sans', system-ui, sans-serif;
  --font-mono: 'DM Mono', monospace;
  --transition-fast: 150ms ease; --transition-base: 250ms ease;
  --transition-slow: 400ms ease;
  --space-xs: 4px; --space-sm: 8px; --space-md: 16px;
  --space-lg: 24px; --space-xl: 40px; --space-2xl: 64px;
}
```

---

*Design System v1.0 — NutriWell · Inspired by the European Kingfisher · Built for health-conscious adults*
