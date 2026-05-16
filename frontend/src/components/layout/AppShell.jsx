import TopNav from "./TopNav";

export default function AppShell({ children }) {
  return (
    <div className="min-h-screen bg-main">
      <TopNav />
      <main className="pt-14 min-h-screen">{children}</main>
    </div>
  );
}
