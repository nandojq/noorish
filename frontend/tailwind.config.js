/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        // Remapped to kingfisher palette — existing class names kept for component compatibility
        main:    "#F0F4F5",   // Soft Cloud
        light:   "#E8EEF0",   // Pearl Mist (surface)
        "surface-up":   "#F5F8F9",
        "surface-down": "#D8E2E6",
        dark:    "#2E3D42",   // Deep Slate
        "text-mid":  "#5A7A85", // Storm Blue
        "text-low":  "#9BB4BC", // Pale Haze
        primary:      "#7FB5C8", // Kingfisher Blue
        "primary-dark": "#5A9AB5",
        secondary:    "#6ECFC0", // Teal Crown
        accent:  "#E8A87C",   // Amber Breast
        "accent-light": "#F5C9A8",
        green:   "#89C4A0",   // Sage Reed
        border:  "#D8E2E6",   // Surface Down
        deficient: "#E07C7C", // Coral Dusk
        excess:    "#E8A87C", // Amber Wing (same as accent)
        success:   "#89C4A0",
        warning:   "#E8A87C",
        error:     "#E07C7C",
      },
      fontFamily: {
        display: ["Lora", "Georgia", "serif"],
        body:    ["DM Sans", "system-ui", "sans-serif"],
        mono:    ["DM Mono", "monospace"],
        sans:    ["DM Sans", "system-ui", "sans-serif"],
      },
      borderRadius: {
        "radius-sm":  "8px",
        "radius-md":  "14px",
        "radius-lg":  "20px",
        "radius-xl":  "28px",
        "radius-pill": "999px",
        xl: "20px",
        lg: "14px",
      },
      boxShadow: {
        raised:    "6px 6px 14px #C8D4D8, -6px -6px 14px #FFFFFF",
        "raised-sm": "3px 3px 8px #C8D4D8, -3px -3px 8px #FFFFFF",
        inset:     "inset 4px 4px 10px #C8D4D8, inset -4px -4px 10px #FFFFFF",
        "inset-sm": "inset 2px 2px 6px #C8D4D8, inset -2px -2px 6px #FFFFFF",
        pressed:   "inset 3px 3px 8px #B8C8CE, inset -3px -3px 8px #FFFFFF",
        elevated:  "10px 10px 20px #C0CCCE, -10px -10px 20px #FFFFFF",
      },
    },
  },
  plugins: [],
};
