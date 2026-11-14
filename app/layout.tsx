import ThemeShell from "./components/ThemeShell";
import "./globals.css";

export const metadata = {
  title: "Solid Integrations LLC",
  description:
    "Operational governance, workflow coordination, and automation for complex vendor and project environments.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <ThemeShell>{children}</ThemeShell>
      </body>
    </html>
  );
}
