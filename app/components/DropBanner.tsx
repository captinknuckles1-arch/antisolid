export default function DropBanner({ until }: { until: string }) {
  if (Date.now() > new Date(until).getTime()) return null;
  return (
    <div style={{ padding: "1rem", background: "var(--accent)", color: "#000", textAlign: "center" }}>
      NEW ISSUE LIVE
    </div>
  );
}
