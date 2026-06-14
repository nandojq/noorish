# 🌿 Noorish — Frontend Design System & Styling Guide

> A clean, modern nutrition web application for health-conscious adults.  
> Inspired by the iridescent plumage of the **European Kingfisher** (*Alcedo atthis*).  
> Version 3.0 — Contrast-safe · WCAG AA · Minimal shadows · Border-first depth.

---

## ⚠️ The Two Prime Directives

**1. Readability always wins.**
> "If I squint at this screen, view it in bright sunlight, or reduce brightness to 50% — can I still read every word?"
If no — change the color. No exceptions.

**2. Shadows are medicine, not food.**
> Use one drop when needed. Never coat everything in it.
The whole app feeling blurry is a direct symptom of too many shadows competing with each other. Depth in Noorish is created by **borders and background contrast first**, shadows only when strictly necessary.

---

## 1. Design Philosophy

- **Warmth** — users are on a health journey. The interface should feel like an encouraging companion, never clinical or cold.
- **Clarity** — nutrition data is complex. The UI strips away noise: generous spacing, clean hierarchy, no visual fog.
- **Restraint** — less depth effect is always more. One well-placed border communicates structure better than five overlapping shadows.

---

## 2. Color Palette — The Kingfisher

The European Kingfisher (*Alcedo atthis*) has three defining zones: electric cobalt blue on the back, iridescent teal on the crown, and burnt orange-amber on the breast.

### 2.1 Complete Color Ramps

Each stop is validated for WCAG AA (4.5:1 body text, 3:1 large text).

#### Primary — Kingfisher Blue

| Stop | Hex | Usage |
|------|-----|-------|
| 50 | `#EAF5FB` | Page backgrounds, tinted chip fills |
| 100 | `#B8DFF4` | Hover tints, disabled fills, decorative borders |
| 200 | `#74C0E8` | Dividers, progress bar accents |
| 400 | `#1E9DD6` | Primary buttons, links, active states |
| 600 | `#0F6E9E` | Button hover, strong borders, link text |
| 800 | `#0B4F72` | Text on light blue surfaces |
| 900 | `#063348` | Dark surfaces, top bar background |

**Validated pairings:**
- `#0F6E9E` on white → 5.2:1 ✅ all text
- `#0B4F72` on `#EAF5FB` → 7.4:1 ✅ all text
- `#B8DFF4` on `#063348` → 9.2:1 ✅ all text
- `#EAF5FB` on `#0F6E9E` → 4.7:1 ✅ all text

#### Secondary — Iridescent Teal

| Stop | Hex | Usage |
|------|-----|-------|
| 50 | `#E2F7F4` | Success backgrounds, tag fills |
| 100 | `#9AE5DA` | Decorative accents |
| 200 | `#4DCCC0` | Progress bar fills |
| 400 | `#12A99A` | Success states, confirmed actions |
| 600 | `#0A7A6E` | Teal borders, hover success |
| 800 | `#075A51` | Text on teal surfaces |
| 900 | `#043C36` | Dark teal surfaces |

**Validated pairings:**
- `#075A51` on `#E2F7F4` → 7.8:1 ✅ all text
- `#9AE5DA` on `#043C36` → 8.5:1 ✅ all text

#### Accent — Burnt Orange

| Stop | Hex | Usage |
|------|-----|-------|
| 50 | `#FEF0E6` | Warning backgrounds, CTA tints |
| 100 | `#FACFAA` | Soft hover fills |
| 200 | `#F4A468` | Carb progress bars, decorative |
| 400 | `#E06620` | CTA buttons, warning indicators |
| 600 | `#A84915` | Accent hover, strong orange borders |
| 800 | `#7A340E` | Text on orange surfaces |
| 900 | `#4F2108` | Dark orange surfaces |

**Validated pairings:**
- `#7A340E` on `#FEF0E6` → 8.3:1 ✅ all text
- `#FFFFFF` on `#A84915` → 5.1:1 ✅ all text
- ⚠️ `#FFFFFF` on `#E06620` → 3.4:1 — large/bold text only

#### Neutral — River Stone

| Stop | Hex | Usage |
|------|-----|-------|
| 50 | `#F2F3F4` | Page background |
| 100 | `#D2D5D8` | Card borders, dividers |
| 200 | `#A8ADB3` | Disabled states only |
| 400 | `#6D747C` | Captions, helper text (floor for readable text) |
| 600 | `#454C54` | Body text |
| 800 | `#2A3038` | Headings, primary text |
| 900 | `#161A1F` | Maximum contrast |

**Validated pairings:**
- `#6D747C` on white → 4.6:1 ✅ minimum acceptable
- `#454C54` on white → 7.5:1 ✅ all text
- `#2A3038` on `#F2F3F4` → 10.4:1 ✅ all text

### 2.2 CSS Custom Properties

```css
:root {
  /* ── Surfaces ── */
  --color-bg:            #F2F3F4;
  --color-surface:       #FFFFFF;    /* Cards are white — clean, no tint */
  --color-surface-alt:   #F7F9FA;    /* Zebra rows, secondary panels */
  --color-surface-dark:  #063348;    /* Top bar, dark panels */

  /* ── Kingfisher Blue ── */
  --color-blue-50:   #EAF5FB;
  --color-blue-100:  #B8DFF4;
  --color-blue-200:  #74C0E8;
  --color-blue-400:  #1E9DD6;
  --color-blue-600:  #0F6E9E;
  --color-blue-800:  #0B4F72;
  --color-blue-900:  #063348;

  /* ── Teal ── */
  --color-teal-50:   #E2F7F4;
  --color-teal-100:  #9AE5DA;
  --color-teal-200:  #4DCCC0;
  --color-teal-400:  #12A99A;
  --color-teal-600:  #0A7A6E;
  --color-teal-800:  #075A51;
  --color-teal-900:  #043C36;

  /* ── Orange Accent ── */
  --color-orange-50:  #FEF0E6;
  --color-orange-100: #FACFAA;
  --color-orange-200: #F4A468;
  --color-orange-400: #E06620;
  --color-orange-600: #A84915;
  --color-orange-800: #7A340E;
  --color-orange-900: #4F2108;

  /* ── Neutral ── */
  --color-neutral-50:  #F2F3F4;
  --color-neutral-100: #D2D5D8;
  --color-neutral-200: #A8ADB3;
  --color-neutral-400: #6D747C;
  --color-neutral-600: #454C54;
  --color-neutral-800: #2A3038;
  --color-neutral-900: #161A1F;

  /* ── Semantic Text ── */
  --color-text-high:        #2A3038;   /* headings, primary data */
  --color-text-mid:         #454C54;   /* body text */
  --color-text-low:         #6D747C;   /* captions — this is the floor */
  --color-text-placeholder: #6D747C;   /* inputs */
  --color-text-disabled:    #A8ADB3;   /* truly disabled — never for readable content */

  /* ── Semantic Status ── */
  --color-success:      #12A99A;
  --color-success-bg:   #E2F7F4;
  --color-success-text: #075A51;
  --color-warning:      #E06620;
  --color-warning-bg:   #FEF0E6;
  --color-warning-text: #7A340E;
  --color-error:        #C0392B;
  --color-error-bg:     #FDECEA;
  --color-error-text:   #7B241C;

  /* ── Borders — primary depth tool ── */
  --border-light:    1px solid #D2D5D8;   /* default card border */
  --border-medium:   1px solid #A8ADB3;   /* inputs, dividers */
  --border-strong:   1px solid #6D747C;   /* hover borders */
  --border-focus:    2px solid #1E9DD6;   /* focus rings */
  --border-blue:     1px solid #B8DFF4;   /* blue tinted borders */

  /* ── Shadows — used sparingly, only where listed ── */
  /* ONE shadow per element maximum. Choose border OR shadow, never both. */
  --shadow-card:    0 1px 3px rgba(0, 0, 0, 0.08);   /* cards only */
  --shadow-popover: 0 4px 16px rgba(0, 0, 0, 0.12);  /* dropdowns, tooltips, modals */
  --shadow-button:  0 1px 2px rgba(0, 0, 0, 0.10);   /* primary buttons only */
  /* NO neumorphic double-shadows anywhere in Noorish. */

  /* ── Spacing ── */
  --space-xs:  4px;
  --space-sm:  8px;
  --space-md:  16px;
  --space-lg:  24px;
  --space-xl:  40px;
  --space-2xl: 64px;

  /* ── Border radius ── */
  --radius-sm:   6px;
  --radius-md:   10px;
  --radius-lg:   14px;
  --radius-xl:   20px;
  --radius-pill: 999px;

  /* ── Transitions ── */
  --transition-fast: 120ms ease;
  --transition-base: 200ms ease;
  --transition-slow: 350ms ease;
}
```

---

## 3. Depth System — Borders First, Shadows Last

This is the most important section for avoiding the "blurry app" problem.

### 3.1 The Depth Hierarchy

Use these techniques in order. Stop when the element reads clearly. **Do not stack multiple techniques on one element.**

```
Level 0 — Background contrast
  The page bg (#F2F3F4) is slightly grey. White cards (#FFFFFF)
  already stand out without any border or shadow.
  Use this for: primary content cards where space does the work.

Level 1 — Border
  Add var(--border-light) to define the edge.
  Use this for: most cards, all inputs, table containers,
  secondary panels, tags, badges.

Level 2 — Shadow (only if border alone isn't enough)
  Add var(--shadow-card) — a single, very subtle drop shadow.
  Use this for: interactive cards that need to feel clickable,
  the primary CTA button.

Level 3 — Elevation shadow (popovers only)
  Add var(--shadow-popover).
  Use this for: dropdown menus, date pickers, tooltips, modals.
  Never on static page elements.
```

### 3.2 What Gets What

| Element | Depth technique | Shadow? |
|---------|----------------|---------|
| Page background | — | ❌ |
| Content card (static) | `--border-light` only | ❌ |
| Content card (clickable) | `--border-light` + `--shadow-card` | ✅ subtle |
| Data table container | `--border-light` only | ❌ |
| Table rows | bottom border divider only | ❌ |
| Search input | `--border-medium` + bg `#F7F9FA` | ❌ |
| Form inputs | `--border-medium` | ❌ |
| Primary button | `--shadow-button` | ✅ subtle |
| Secondary/ghost button | `--border-light` only | ❌ |
| Badges/tags | bg fill + no border, no shadow | ❌ |
| Dropdown / popover | `--shadow-popover` | ✅ |
| Sidebar | right border only | ❌ |
| Top bar | bottom border only | ❌ |
| Progress bar track | bg color change only (`--color-surface-alt`) | ❌ |
| Icon buttons | `--border-light` on hover only | ❌ |
| Modals | `--shadow-popover` | ✅ |

### 3.3 Forbidden Shadow Patterns

```css
/* ❌ NEVER — neumorphic double shadows */
box-shadow: 5px 5px 12px rgba(160,174,180,0.45), -5px -5px 12px rgba(255,255,255,0.90);

/* ❌ NEVER — inset neumorphic shadows on inputs */
box-shadow: inset 3px 3px 8px rgba(160,174,180,0.45), inset -3px -3px 8px rgba(255,255,255,0.90);

/* ❌ NEVER — large blur radius on cards */
box-shadow: 0 8px 24px rgba(0,0,0,0.15);

/* ❌ NEVER — shadow AND border on the same element */
border: 1px solid #D2D5D8;
box-shadow: 0 2px 8px rgba(0,0,0,0.10); /* pick one */

/* ❌ NEVER — coloured shadows */
box-shadow: 4px 4px 10px rgba(95,154,181,0.4), -2px -2px 8px rgba(255,255,255,0.6);

/* ✅ CORRECT — card with border only */
border: 1px solid var(--color-neutral-100);
border-radius: var(--radius-lg);

/* ✅ CORRECT — clickable card */
border: 1px solid var(--color-neutral-100);
border-radius: var(--radius-lg);
box-shadow: var(--shadow-card);   /* 0 1px 3px rgba(0,0,0,0.08) */

/* ✅ CORRECT — dropdown */
border: 1px solid var(--color-neutral-100);
border-radius: var(--radius-md);
box-shadow: var(--shadow-popover);  /* 0 4px 16px rgba(0,0,0,0.12) */
```

---

## 4. Contrast — The Law

### 4.1 WCAG AA Requirements

| Text type | Minimum contrast |
|-----------|-----------------|
| Body text (< 18px or < 14px bold) | 4.5:1 |
| Large text (≥ 18px or ≥ 14px bold) | 3.0:1 |
| UI components, borders on interactive elements | 3.0:1 |

### 4.2 Forbidden Color Combinations

```
❌ Any text ≤ --color-text-low (#6D747C) on dark surfaces
❌ Orange (#E06620) as text color on any background
❌ Teal (#12A99A) as text color on white (only 2.9:1)
❌ --color-text-disabled (#A8ADB3) for any readable content
❌ Section titles in orange on dark blue panels
❌ Dark badge text on dark badge background
❌ Placeholder text lighter than #6D747C
❌ White text on --color-blue-400 (#1E9DD6) for body text (only 3.8:1)
```

### 4.3 Color Pairing Rules

**Light surfaces (white, `--color-bg`, `--color-surface-alt`):**
- Primary text → `--color-text-high` (#2A3038)
- Secondary text → `--color-text-mid` (#454C54)
- Captions/helper → `--color-text-low` (#6D747C) — absolute floor
- Placeholder → `--color-text-placeholder` (#6D747C)
- Links → `--color-blue-600` (#0F6E9E) — not 400

**Dark surfaces (`--color-blue-900` and darker):**
- Primary text → `#FFFFFF`
- Secondary text → `--color-blue-100` (#B8DFF4) — minimum
- Section headings → `#FFFFFF` always — never orange, never teal
- Captions → `--color-blue-200` (#74C0E8) — minimum

**Colored fills (badges, tags, pills):**
- Blue fill (50) → text: `--color-blue-800` ✅
- Teal fill (50) → text: `--color-teal-800` ✅
- Orange fill (50) → text: `--color-orange-800` ✅
- Neutral fill (100) → text: `--color-neutral-800` ✅

---

## 5. Typography

### 5.1 Font Stack

| Role | Font | Weights |
|------|------|---------|
| Display / Headings | **Lora** (Google Fonts) | 500, 600, 700 |
| Body / UI | **DM Sans** (Google Fonts) | 400, 500 |
| Data / Numbers | **DM Mono** (Google Fonts) | 400, 500 |

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Lora:wght@500;600;700&family=DM+Sans:wght@400;500&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">
```

### 5.2 Type Scale

```css
:root {
  --font-display: 'Lora', Georgia, serif;
  --font-body:    'DM Sans', system-ui, sans-serif;
  --font-mono:    'DM Mono', monospace;

  --text-xs:   0.75rem;    /* 12px — badges only */
  --text-sm:   0.875rem;   /* 14px — labels, table cells */
  --text-base: 1rem;       /* 16px — body copy minimum */
  --text-lg:   1.125rem;   /* 18px — lead text */
  --text-xl:   1.375rem;   /* 22px — card headings */
  --text-2xl:  1.75rem;    /* 28px — section titles */
  --text-3xl:  2.25rem;    /* 36px — page headings */
  --text-4xl:  3rem;       /* 48px — hero display */

  --leading-tight:  1.2;   /* headings only */
  --leading-normal: 1.6;   /* body text minimum */
  --leading-loose:  1.8;
}

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
  font-weight: 600;
}

h4, h5, h6, label, button {
  font-family: var(--font-body);
  font-weight: 500;
  color: var(--color-text-mid);
}

.data-value {
  font-family: var(--font-mono);
  font-weight: 500;
  letter-spacing: -0.02em;
  color: var(--color-text-high);
}
```

### 5.3 Typography Rules

- Body copy: minimum `--text-base` (16px), never smaller
- UI labels, form labels: minimum `--text-sm` (14px)
- Table cell data: minimum `--text-sm` (14px)
- Badges, captions: `--text-xs` (12px) only for supplemental info
- Body line-height: minimum `1.6` — never `1.2` for body text
- Never use `font-weight: 300` — too thin to read at small sizes

---

## 6. Component Library

### 6.1 Cards

```css
/* Standard card — white on grey page bg, border only */
.card {
  background: var(--color-surface);       /* #FFFFFF */
  border: var(--border-light);            /* 1px solid #D2D5D8 */
  border-radius: var(--radius-lg);
  padding: var(--space-lg);
}

/* Clickable card — add minimal shadow */
.card--interactive {
  background: var(--color-surface);
  border: var(--border-light);
  border-radius: var(--radius-lg);
  padding: var(--space-lg);
  box-shadow: var(--shadow-card);         /* 0 1px 3px rgba(0,0,0,0.08) */
  cursor: pointer;
  transition: border-color var(--transition-fast),
              box-shadow var(--transition-fast),
              transform var(--transition-fast);
}

.card--interactive:hover {
  border-color: var(--color-blue-200);    /* Blue border tint on hover */
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.10);
  transform: translateY(-1px);
}

/* Card heading */
.card__title {
  font-family: var(--font-display);
  font-size: var(--text-xl);
  color: var(--color-text-high);
  font-weight: 600;
  margin-bottom: var(--space-xs);
}

.card__subtitle {
  font-size: var(--text-sm);
  color: var(--color-text-mid);
}

/* Inner section panel — tinted bg, no border or shadow */
.card__section {
  background: var(--color-surface-alt);   /* #F7F9FA */
  border-radius: var(--radius-md);
  padding: var(--space-md);
}

.card__section + .card__section {
  margin-top: var(--space-sm);
}
```

### 6.2 Dark Panels (Settings, Recipe Forms)

Dark panels use flat design — borders for structure, no shadows, no neumorphism.

```css
.panel--dark {
  background: var(--color-blue-900);      /* #063348 */
  border-radius: var(--radius-lg);
  padding: var(--space-lg);
  /* No shadow — the dark bg contrasts enough with the page */
}

/* Section heading inside dark panel — WHITE, never orange */
.panel--dark .panel__title {
  font-family: var(--font-display);
  font-size: var(--text-lg);
  font-weight: 600;
  color: #FFFFFF;
  margin-bottom: var(--space-sm);
  padding-bottom: var(--space-sm);
  border-bottom: 1px solid rgba(255, 255, 255, 0.12);
}

/* Body text in dark panel */
.panel--dark p,
.panel--dark .description {
  color: var(--color-blue-100);           /* #B8DFF4 — 9.2:1 ✅ */
  font-size: var(--text-base);
  line-height: var(--leading-normal);
}

/* Sub-section divider inside dark panel */
.panel--dark .panel__divider {
  border: none;
  border-top: 1px solid rgba(255, 255, 255, 0.10);
  margin: var(--space-md) 0;
}

/* Inputs inside dark panel — flat with explicit border */
.panel--dark .input-field {
  background: rgba(255, 255, 255, 0.07);
  border: 1px solid rgba(255, 255, 255, 0.20);
  border-radius: var(--radius-sm);
  color: #FFFFFF;
  font-size: var(--text-base);
  padding: 11px 14px;
  box-shadow: none;                       /* No shadow inside dark panels */
  outline: none;
  transition: border-color var(--transition-fast);
}

.panel--dark .input-field::placeholder {
  color: var(--color-blue-200);           /* #74C0E8 — visible, not ghost */
}

.panel--dark .input-field:focus {
  border-color: var(--color-blue-200);
  background: rgba(255, 255, 255, 0.10);
}

/* Labels in dark panel */
.panel--dark .input-label {
  font-size: var(--text-sm);
  font-weight: 500;
  color: var(--color-blue-100);
  display: block;
  margin-bottom: var(--space-xs);
}

/* Sub-heading labels (like "Deficiency threshold") — NOT orange */
.panel--dark .field-label {
  font-size: var(--text-sm);
  font-weight: 500;
  color: var(--color-blue-100);           /* Blue-tinted white ✅ */
}

.panel--dark .field-description {
  font-size: var(--text-sm);
  color: var(--color-blue-200);           /* #74C0E8 ✅ */
  line-height: var(--leading-normal);
}
```

### 6.3 Data Tables

The ingredients table fix — border-only structure, high-contrast text everywhere.

```css
/* Container — white card, border only */
.data-table-wrap {
  background: var(--color-surface);
  border: var(--border-light);
  border-radius: var(--radius-lg);
  overflow: hidden;
  /* No shadow — border is enough on the grey page bg */
}

/* Column headers */
.data-table thead th {
  background: var(--color-blue-900);
  color: var(--color-blue-100);           /* #B8DFF4 — 9.2:1 ✅ */
  font-family: var(--font-body);
  font-size: 11px;
  font-weight: 500;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  padding: 12px var(--space-md);
  text-align: left;
  border-bottom: 2px solid var(--color-blue-800);
}

/* Rows */
.data-table tbody tr {
  border-bottom: var(--border-light);
  transition: background var(--transition-fast);
}

.data-table tbody tr:last-child {
  border-bottom: none;
}

.data-table tbody tr:hover {
  background: var(--color-blue-50);       /* Subtle blue tint ✅ */
}

/* Cell types */
.data-table td {
  padding: 13px var(--space-md);
  vertical-align: middle;
}

.data-table td.cell--primary {
  font-size: var(--text-sm);
  font-weight: 500;
  color: var(--color-text-high);          /* #2A3038 ✅ */
}

.data-table td.cell--category {
  font-size: var(--text-sm);
  color: var(--color-blue-600);           /* #0F6E9E — 5.2:1 ✅ */
}

.data-table td.cell--number {
  font-family: var(--font-mono);
  font-size: var(--text-sm);
  color: var(--color-text-mid);           /* #454C54 ✅ */
}

.data-table td.cell--source {
  font-size: var(--text-xs);
  color: var(--color-text-low);           /* #6D747C — 4.6:1, floor ✅ */
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

/* Quality badges — light fill + dark text from same ramp */
.badge--quality {
  display: inline-flex;
  align-items: center;
  padding: 3px 10px;
  border-radius: var(--radius-pill);
  font-size: var(--text-xs);
  font-weight: 500;
  /* No shadow on badges */
}

.badge--high   { background: var(--color-teal-50);    color: var(--color-teal-800);   }
.badge--medium { background: var(--color-blue-50);    color: var(--color-blue-800);   }
.badge--low    { background: var(--color-orange-50);  color: var(--color-orange-800); }
```

### 6.4 Buttons

```css
/* Primary — filled blue */
.btn-primary {
  font-family: var(--font-body);
  font-weight: 500;
  font-size: var(--text-sm);
  color: #FFFFFF;
  background: var(--color-blue-400);
  border: none;
  border-radius: var(--radius-pill);
  padding: 11px 24px;
  min-height: 44px;
  cursor: pointer;
  box-shadow: var(--shadow-button);       /* Only button that gets a shadow */
  transition: background var(--transition-fast), transform var(--transition-fast);
}

.btn-primary:hover {
  background: var(--color-blue-600);
  transform: translateY(-1px);
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.14);
}

.btn-primary:active {
  background: var(--color-blue-800);
  transform: translateY(0);
  box-shadow: none;
}

/* Secondary — border only, no shadow */
.btn-secondary {
  font-family: var(--font-body);
  font-weight: 500;
  font-size: var(--text-sm);
  color: var(--color-blue-800);
  background: transparent;
  border: var(--border-light);
  border-radius: var(--radius-pill);
  padding: 11px 24px;
  min-height: 44px;
  cursor: pointer;
  transition: border-color var(--transition-fast),
              background var(--transition-fast);
  box-shadow: none;                       /* No shadow on secondary buttons */
}

.btn-secondary:hover {
  border-color: var(--color-blue-400);
  background: var(--color-blue-50);
  color: var(--color-blue-600);
}

.btn-secondary:active {
  background: var(--color-blue-100);
}

/* Accent CTA — orange */
.btn-accent {
  font-family: var(--font-body);
  font-weight: 500;
  font-size: var(--text-sm);
  color: #FFFFFF;
  background: var(--color-orange-600);    /* 600 for white text contrast ✅ */
  border: none;
  border-radius: var(--radius-pill);
  padding: 11px 24px;
  min-height: 44px;
  cursor: pointer;
  box-shadow: var(--shadow-button);
  transition: background var(--transition-fast), transform var(--transition-fast);
}

.btn-accent:hover {
  background: var(--color-orange-800);
  transform: translateY(-1px);
}

.btn-accent:active {
  transform: translateY(0);
  box-shadow: none;
}

/* Ghost / icon button */
.btn-ghost {
  font-family: var(--font-body);
  font-weight: 500;
  font-size: var(--text-sm);
  color: var(--color-text-mid);
  background: transparent;
  border: none;
  border-radius: var(--radius-md);
  padding: 10px 16px;
  min-height: 44px;
  cursor: pointer;
  box-shadow: none;
  transition: background var(--transition-fast), color var(--transition-fast);
}

.btn-ghost:hover {
  background: var(--color-neutral-100);
  color: var(--color-text-high);
}
```

### 6.5 Inputs & Form Fields

```css
/* Label — always a visible element above the input */
.input-label {
  font-size: var(--text-sm);
  font-weight: 500;
  color: var(--color-text-mid);
  display: block;
  margin-bottom: var(--space-xs);
}

/* Standard input — border only, no shadow */
.input-field {
  width: 100%;
  font-family: var(--font-body);
  font-size: var(--text-base);
  color: var(--color-text-high);
  background: var(--color-surface-alt);   /* Slightly off-white to show it's editable */
  border: var(--border-medium);           /* 1px solid #A8ADB3 */
  border-radius: var(--radius-md);
  padding: 11px 14px;
  min-height: 44px;
  outline: none;
  box-shadow: none;                       /* No inset shadow — border is enough */
  transition: border-color var(--transition-fast),
              background var(--transition-fast);
}

.input-field::placeholder {
  color: var(--color-text-placeholder);   /* #6D747C — always readable ✅ */
}

.input-field:hover {
  border-color: var(--color-neutral-400);
}

.input-field:focus {
  border-color: var(--color-blue-400);
  border-width: 2px;
  background: var(--color-surface);       /* White on focus */
  padding: 10px 13px;                     /* Compensate for border-width increase */
}

/* Error state */
.input-field--error {
  border-color: var(--color-error);
}

.input-error-msg {
  font-size: var(--text-xs);
  color: var(--color-error-text);
  margin-top: var(--space-xs);
}

/* Search bar — same pattern */
.input-search {
  background: var(--color-surface);
  border: var(--border-light);
  /* Everything else inherits from .input-field */
}

/* Select */
.select-field {
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='14' height='14' viewBox='0 0 24 24' fill='none' stroke='%232A3038' stroke-width='2'%3E%3Cpolyline points='6 9 12 15 18 9'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 12px center;
  background-color: var(--color-surface-alt);
  padding-right: 38px;
  cursor: pointer;
}

/* RULE: Labels must ALWAYS be visible <label> elements.
   Never rely on placeholder text as a substitute.
   Placeholder vanishes on focus — users lose context. */
```

### 6.6 Nutrient Progress Bars

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
  font-weight: 500;
  color: var(--color-text-high);
}

/* Track — background color change only, no shadow */
.nutrient-bar {
  height: 8px;
  border-radius: var(--radius-pill);
  background: var(--color-neutral-100);   /* Simple grey track */
  overflow: hidden;
}

.nutrient-bar__fill {
  height: 100%;
  border-radius: var(--radius-pill);
  transition: width var(--transition-slow);
  animation: fillBar 0.7s ease forwards;
}

.nutrient-bar__fill--protein  { background: var(--color-blue-400); }
.nutrient-bar__fill--carbs    { background: var(--color-orange-400); }
.nutrient-bar__fill--fat      { background: var(--color-teal-400); }
.nutrient-bar__fill--calories { background: var(--color-blue-600); }
.nutrient-bar__fill--warning  { background: var(--color-orange-400); }
.nutrient-bar__fill--over     { background: var(--color-error); }
```

### 6.7 Tags & Badges

```css
/* All tags — bg fill only, no border, no shadow */
.tag {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: var(--text-xs);
  font-weight: 500;
  padding: 3px 10px;
  border-radius: var(--radius-pill);
  /* box-shadow: none — always */
}

/* Ramp rule: 50-stop fill + 800-stop text from same ramp */
.tag--protein  { background: var(--color-blue-50);    color: var(--color-blue-800);   }
.tag--vegan    { background: var(--color-teal-50);    color: var(--color-teal-800);   }
.tag--highcal  { background: var(--color-orange-50);  color: var(--color-orange-800); }
.tag--lowcarb  { background: var(--color-blue-50);    color: var(--color-blue-800);   }
.tag--manual   { background: var(--color-neutral-100); color: var(--color-neutral-800); }
```

### 6.8 Colour Coding Guide / Legend

Fix for the Settings screen where legend text was invisible:

```css
.legend-item {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  padding: 6px 0;
  border-bottom: var(--border-light);
}

.legend-item:last-child {
  border-bottom: none;
}

.legend-item__dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
}

/* Range label — body text color, never the dot color */
.legend-item__range {
  font-size: var(--text-sm);
  font-weight: 500;
  color: var(--color-text-mid);           /* #454C54 on light ✅ */
  min-width: 110px;
}

/* On dark panels, override with light text */
.panel--dark .legend-item__range {
  color: var(--color-blue-100);           /* #B8DFF4 ✅ */
}

.legend-item__status {
  font-size: var(--text-sm);
  color: var(--color-text-low);           /* #6D747C ✅ */
}

.panel--dark .legend-item__status {
  color: var(--color-blue-200);           /* #74C0E8 ✅ */
}

/* RULE: The dot color is decorative. Text must be readable independently.
   Never set text color to match the dot color on a dark background. */
```

### 6.9 Icon Buttons

```css
.icon-btn {
  width: 36px;
  height: 36px;
  min-width: 44px;
  min-height: 44px;
  border-radius: var(--radius-md);
  background: transparent;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: var(--color-text-mid);
  box-shadow: none;
  transition: background var(--transition-fast), color var(--transition-fast);
}

.icon-btn:hover {
  background: var(--color-neutral-100);
  color: var(--color-text-high);
}

.icon-btn:active {
  background: var(--color-neutral-200);
}
```

---

## 7. Layout System

### 7.1 App Layout

```css
.page-wrapper {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 var(--space-xl);
}

.app-layout {
  display: grid;
  grid-template-columns: 240px 1fr;
  grid-template-rows: 56px 1fr;
  grid-template-areas:
    "sidebar topbar"
    "sidebar main";
  min-height: 100vh;
}

@media (max-width: 900px) {
  .app-layout {
    grid-template-columns: 1fr;
    grid-template-areas: "topbar" "main";
  }
}
```

### 7.2 Top Bar

```css
.topbar {
  grid-area: topbar;
  background: var(--color-blue-900);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 var(--space-xl);
  border-bottom: 1px solid var(--color-blue-800);
  /* No shadow — border-bottom is the separator */
}

.topbar__brand {
  font-family: var(--font-display);
  font-size: var(--text-xl);
  font-weight: 700;
  color: #FFFFFF;
}

.topbar__nav-link {
  font-size: var(--text-sm);
  font-weight: 500;
  color: var(--color-blue-100);           /* #B8DFF4 ✅ */
  text-decoration: none;
  padding: 6px 12px;
  border-radius: var(--radius-sm);
  transition: color var(--transition-fast), background var(--transition-fast);
}

.topbar__nav-link:hover {
  color: #FFFFFF;
  background: rgba(255, 255, 255, 0.08);
}

.topbar__nav-link--active {
  color: #FFFFFF;
  border-bottom: 2px solid var(--color-orange-400);
  padding-bottom: 4px;
}
```

### 7.3 Sidebar

```css
.sidebar {
  grid-area: sidebar;
  background: var(--color-surface);       /* White sidebar */
  border-right: var(--border-light);      /* Right border — no shadow */
  padding: var(--space-xl) var(--space-md);
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: var(--space-md);
  padding: 10px var(--space-md);
  border-radius: var(--radius-md);
  font-weight: 500;
  font-size: var(--text-sm);
  color: var(--color-text-mid);
  text-decoration: none;
  transition: background var(--transition-fast), color var(--transition-fast);
  cursor: pointer;
  box-shadow: none;                       /* No shadow on nav items */
}

.nav-item:hover {
  background: var(--color-blue-50);
  color: var(--color-blue-600);
}

.nav-item--active {
  background: var(--color-blue-50);
  color: var(--color-blue-800);
  font-weight: 500;
  border-left: 3px solid var(--color-blue-400);
  padding-left: calc(var(--space-md) - 3px);
}
```

---

## 8. Iconography

Use **Phosphor Icons** — warm, rounded style that suits Noorish's character.

```html
<script src="https://unpkg.com/@phosphor-icons/web"></script>
<i class="ph ph-bowl-food"></i>
<i class="ph ph-carrot"></i>
<i class="ph ph-chart-pie"></i>
<i class="ph ph-calendar-blank"></i>
<i class="ph ph-fire"></i>
```

---

## 9. Dark Mode

```css
@media (prefers-color-scheme: dark) {
  :root {
    --color-bg:           #161A1F;
    --color-surface:      #1E252B;
    --color-surface-alt:  #252D35;
    --color-surface-dark: #063348;

    --color-text-high:        #E8F2F6;
    --color-text-mid:         #9BBAC4;
    --color-text-low:         #6D8A94;
    --color-text-placeholder: #6D8A94;
    --color-text-disabled:    #3A5058;

    --border-light:   1px solid rgba(255, 255, 255, 0.10);
    --border-medium:  1px solid rgba(255, 255, 255, 0.18);
    --border-strong:  1px solid rgba(255, 255, 255, 0.30);

    /* Shadows stay minimal in dark mode too */
    --shadow-card:    0 1px 3px rgba(0, 0, 0, 0.30);
    --shadow-popover: 0 4px 16px rgba(0, 0, 0, 0.45);
    --shadow-button:  0 1px 2px rgba(0, 0, 0, 0.30);
  }
}
```

---

## 10. Motion

Keep animations purposeful and gentle.

```css
@keyframes fadeSlideUp {
  from { opacity: 0; transform: translateY(12px); }
  to   { opacity: 1; transform: translateY(0); }
}

.animate-in { animation: fadeSlideUp 0.35s ease forwards; }

/* Stagger page sections */
.card:nth-child(1) { animation-delay: 0ms;   }
.card:nth-child(2) { animation-delay: 50ms;  }
.card:nth-child(3) { animation-delay: 100ms; }
.card:nth-child(4) { animation-delay: 150ms; }

@keyframes fillBar {
  from { width: 0%; }
}

.skeleton {
  background: var(--color-neutral-100);
  border-radius: var(--radius-sm);
  animation: pulse 1.5s ease infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1;   }
  50%       { opacity: 0.5; }
}

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## 11. Accessibility

```css
:focus-visible {
  outline: 2px solid var(--color-blue-400);
  outline-offset: 3px;
  border-radius: var(--radius-sm);
}

button, a, [role="button"] {
  min-height: 44px;
  min-width: 44px;
}
```

- Never write `outline: none` without a custom `:focus-visible` replacement
- Color must never be the only way to convey status — pair with icon or text label
- All images must have `alt` text; decorative images use `alt=""`
- Every `<input>` must have an explicit `<label>` — placeholder is not a label
- Table headers must use `<th scope="col">` or `<th scope="row">`

---

## 12. Pre-Ship Checklist

Run this before merging any UI change:

```
SHADOWS
□ No neumorphic double-shadow (dark + white) anywhere
□ No inset neumorphic shadows on inputs
□ Cards use border only OR border + --shadow-card (never both heavy)
□ Only dropdowns/modals use --shadow-popover
□ No coloured shadows
□ No element has both a border and a heavy shadow

CONTRAST & TYPOGRAPHY
□ All body text ≥ 16px and ≥ 4.5:1 on its background
□ All labels and table cells ≥ 14px and ≥ 4.5:1
□ Placeholder text uses --color-text-placeholder (#6D747C)
□ No text uses --color-text-disabled for readable content
□ Every input has a visible <label> element above it

DARK PANELS
□ Section titles use #FFFFFF — not orange, not teal
□ Body text uses --color-blue-100 (#B8DFF4) or brighter
□ Inputs inside dark panels use flat border style, no neumorphic shadow
□ Legend/guide text uses --color-blue-100 or --color-blue-200

BADGES & TAGS
□ Every badge uses 50-stop fill + 800-stop text from same ramp
□ No badge has dark fill + dark text

INTERACTIVE
□ Every button has hover, active, focus-visible states
□ Every input has focus state with visible border change
□ Minimum 44×44px touch target on all interactive elements
□ No pure #000000 — use --color-text-high (#2A3038)
```

---

## 13. Quick-Reference Token Sheet

Paste at the top of your main CSS file:

```css
:root {
  /* Surfaces */
  --color-bg: #F2F3F4;
  --color-surface: #FFFFFF;
  --color-surface-alt: #F7F9FA;
  --color-surface-dark: #063348;

  /* Kingfisher Blue */
  --color-blue-50: #EAF5FB;   --color-blue-100: #B8DFF4;
  --color-blue-200: #74C0E8;  --color-blue-400: #1E9DD6;
  --color-blue-600: #0F6E9E;  --color-blue-800: #0B4F72;
  --color-blue-900: #063348;

  /* Teal */
  --color-teal-50: #E2F7F4;   --color-teal-100: #9AE5DA;
  --color-teal-200: #4DCCC0;  --color-teal-400: #12A99A;
  --color-teal-600: #0A7A6E;  --color-teal-800: #075A51;
  --color-teal-900: #043C36;

  /* Orange */
  --color-orange-50: #FEF0E6;   --color-orange-100: #FACFAA;
  --color-orange-200: #F4A468;  --color-orange-400: #E06620;
  --color-orange-600: #A84915;  --color-orange-800: #7A340E;
  --color-orange-900: #4F2108;

  /* Neutral */
  --color-neutral-50: #F2F3F4;   --color-neutral-100: #D2D5D8;
  --color-neutral-200: #A8ADB3;  --color-neutral-400: #6D747C;
  --color-neutral-600: #454C54;  --color-neutral-800: #2A3038;
  --color-neutral-900: #161A1F;

  /* Text */
  --color-text-high: #2A3038;  --color-text-mid: #454C54;
  --color-text-low: #6D747C;   --color-text-placeholder: #6D747C;
  --color-text-disabled: #A8ADB3;

  /* Status */
  --color-success: #12A99A;  --color-success-bg: #E2F7F4;  --color-success-text: #075A51;
  --color-warning: #E06620;  --color-warning-bg: #FEF0E6;  --color-warning-text: #7A340E;
  --color-error: #C0392B;    --color-error-bg: #FDECEA;    --color-error-text: #7B241C;

  /* Borders — primary depth tool */
  --border-light:  1px solid #D2D5D8;
  --border-medium: 1px solid #A8ADB3;
  --border-strong: 1px solid #6D747C;
  --border-focus:  2px solid #1E9DD6;
  --border-blue:   1px solid #B8DFF4;

  /* Shadows — use sparingly, only where listed */
  --shadow-card:    0 1px 3px rgba(0,0,0,0.08);
  --shadow-popover: 0 4px 16px rgba(0,0,0,0.12);
  --shadow-button:  0 1px 2px rgba(0,0,0,0.10);

  /* Typography */
  --font-display: 'Lora', Georgia, serif;
  --font-body: 'DM Sans', system-ui, sans-serif;
  --font-mono: 'DM Mono', monospace;

  /* Spacing */
  --space-xs: 4px;  --space-sm: 8px;   --space-md: 16px;
  --space-lg: 24px; --space-xl: 40px;  --space-2xl: 64px;

  /* Radius */
  --radius-sm: 6px;  --radius-md: 10px;  --radius-lg: 14px;
  --radius-xl: 20px; --radius-pill: 999px;

  /* Motion */
  --transition-fast: 120ms ease;
  --transition-base: 200ms ease;
  --transition-slow: 350ms ease;
}
```

---

*Design System v3.0 — Noorish · Kingfisher palette · WCAG AA · Border-first depth · No visual fog*