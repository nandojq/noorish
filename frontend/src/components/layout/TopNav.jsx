import { Link, useMatch } from "react-router-dom";
import { GearSix } from "@phosphor-icons/react";
import { useMenus } from "@/hooks/useMenus";

const NAV_LINKS = [
  { label: "Menu", to: "/menus" },
  { label: "Recipes", to: "/recipes" },
  { label: "Ingredients", to: "/ingredients" },
  { label: "Analysis", to: "/analysis" },
  { label: "Grocery", to: "/grocery" },
];

function NavLink({ to, label }) {
  const match = useMatch({ path: to, end: false });
  return (
    <Link
      to={to}
      style={{
        fontFamily: "var(--font-body)",
        fontSize: "0.875rem",
        fontWeight: 500,
        color: match ? "var(--kf-orange-400)" : "var(--color-nav-text)",
        borderBottom: match ? "2px solid var(--kf-orange-400)" : "2px solid transparent",
        paddingBottom: "2px",
        textDecoration: "none",
        transition: "color var(--transition-fast)",
        letterSpacing: "0.01em",
      }}
    >
      {label}
    </Link>
  );
}

export default function TopNav() {
  const { data: menus } = useMenus();
  const firstMenuId = menus?.[0]?.id;

  const resolveLink = (label, to) => {
    if (label === "Analysis" && firstMenuId) return `/analysis/${firstMenuId}`;
    if (label === "Grocery" && firstMenuId) return `/grocery/${firstMenuId}`;
    return to;
  };

  return (
    <nav
      style={{ background: "var(--color-nav-bg)" }}
      className="fixed top-0 left-0 right-0 z-40 h-14 flex items-center px-6 gap-10 border-b border-border"
    >
      <Link
        to="/"
        style={{ fontFamily: "var(--font-display)", fontSize: "1.375rem", fontWeight: 700, color: "var(--kf-blue-50)", letterSpacing: "-0.01em", textDecoration: "none" }}
        className="shrink-0"
      >
        Noorish
      </Link>

      <div className="flex items-center gap-7 flex-1 justify-center">
        {NAV_LINKS.map(({ label, to }) => (
          <NavLink key={label} to={resolveLink(label, to)} label={label} />
        ))}
      </div>

      <Link
        to="/settings"
        style={{ color: "var(--color-nav-text-dim)", transition: "color var(--transition-fast)" }}
        onMouseOver={(e) => (e.currentTarget.style.color = "var(--kf-orange-400)")}
        onMouseOut={(e) => (e.currentTarget.style.color = "var(--color-nav-text-dim)")}
        aria-label="Settings"
      >
        <GearSix size={22} weight="regular" />
      </Link>
    </nav>
  );
}
