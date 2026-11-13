export default function SolidIntegrationsPortal() {
  return (
    <main
      style={{
        backgroundColor: '#101312',
        color: '#edf2ed',
        fontFamily: 'system-ui, sans-serif',
        minHeight: '100vh',
        padding: 'clamp(24px, 5vw, 64px) 20px',
      }}
    >
      <div style={{ maxWidth: 900, margin: '0 auto' }}>
        <header style={{ borderBottom: '1px solid #344139', paddingBottom: 24 }}>
          <p style={{ color: '#8dbb8e', letterSpacing: '0.14em', textTransform: 'uppercase' }}>
            Solid Integrations LLC
          </p>
          <h1 style={{ fontSize: 'clamp(2.2rem, 6vw, 4rem)', lineHeight: 1.05, margin: '12px 0' }}>
            Governance before scale.
          </h1>
          <p style={{ color: '#b4c0b7', maxWidth: 700, lineHeight: 1.7 }}>
            Operational governance, workflow coordination, and automation for complex vendor and project environments.
          </p>
        </header>

        <section style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: 16, marginTop: 32 }}>
          <article style={{ background: '#191f1b', border: '1px solid #344139', padding: 22 }}>
            <h2 style={{ color: '#8dbb8e' }}>Solid+ governance</h2>
            <p style={{ color: '#b4c0b7', lineHeight: 1.6 }}>
              Workflow controls, approvals, exception handling, audit trails, and operating reports.
            </p>
          </article>
          <article style={{ background: '#191f1b', border: '1px solid #344139', padding: 22 }}>
            <h2 style={{ color: '#8dbb8e' }}>Energy project coordination</h2>
            <p style={{ color: '#b4c0b7', lineHeight: 1.6 }}>
              Feasibility, partner coordination, and documentation with appropriately authorized providers responsible for regulated services and field fulfillment.
            </p>
          </article>
          <article style={{ background: '#191f1b', border: '1px solid #344139', padding: 22 }}>
            <h2 style={{ color: '#8dbb8e' }}>Operations automation</h2>
            <p style={{ color: '#b4c0b7', lineHeight: 1.6 }}>
              Process mapping, vendor records, reporting workflows, and measurable operational controls.
            </p>
          </article>
        </section>

        <section style={{ marginTop: 32, borderTop: '1px solid #344139', paddingTop: 24 }}>
          <p style={{ color: '#b4c0b7', lineHeight: 1.7 }}>
            Each engagement is defined by a written scope, verified capabilities, and mutually agreed commercial terms. Solid Integrations does not represent itself as a utility, retail electricity provider, installer, lender, or government administrator.
          </p>
          <p style={{ marginTop: 24 }}>
            Business inquiries: <a style={{ color: '#8dbb8e' }} href="mailto:solid.lp@outlook.com">solid.lp@outlook.com</a>
          </p>
        </section>

        <footer style={{ borderTop: '1px solid #344139', marginTop: 48, paddingTop: 16, color: '#7f8d82', fontSize: 13 }}>
          © 2026 Solid Integrations LLC. All rights reserved.
        </footer>
      </div>
    </main>
  );
}
