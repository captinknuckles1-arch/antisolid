export default function CoverHero({ title }: { title: string }) {
  return (
    <section style={{ marginBottom: "3rem", borderBottom: "1px solid #222" }}>
      <h1 style={{ fontSize: "3rem", letterSpacing: "0.2em" }}>{title}</h1>
      <div style={{ color: "var(--accent)", marginTop: "1rem" }}>CURRENT ISSUE</div>
    </section>
  );
}
