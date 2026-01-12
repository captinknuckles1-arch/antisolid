import ThemeShell from "./components/ThemeShell";
import "./globals.css";

export const metadata = {
  title: "ANTISOLID",
  description: "Skate / Tattoos / Metal / Moto / Underground",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <header className="nav">
          <div className="brand">ANTISOLID</div>
          <nav>
            <a href="/">Home</a>
            <a href="/issues">Issues</a>
            <a href="/shop">Shop</a>
            <a href="/search">Search</a>
          </nav>
        </header>
        <ThemeShell><main>{children}</main></ThemeShell>
        <footer className="footer">
          © ANTISOLID — ARCHIVE
        </footer>
      </body>
    </html>
  );
}
