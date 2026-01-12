import fs from "fs";
import path from "path";
import { THEMES } from "@/app/theme";

export default function ThemeShell({ children }: { children: React.ReactNode }) {
  const editionsDir = path.join(process.cwd(), "content/editions");
  const editions = fs.readdirSync(editionsDir).sort().reverse();
  const latest = editions[0];

  let themeKey = "default";
  try {
    const meta = JSON.parse(
      fs.readFileSync(path.join(editionsDir, latest, "meta.json"), "utf8")
    );
    themeKey = meta.theme || "default";
  } catch {}

  const t = THEMES[themeKey] || THEMES.default;

  return (
    <div style={{ background: t.bg, color: t.fg, minHeight: "100vh" }}>
      <style>{`:root{--accent:${t.accent};}`}</style>
      {children}
    </div>
  );
}
