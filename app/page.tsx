import fs from 'fs';
import path from 'path';
import { notFound } from 'next/navigation';

export default function Home() {
  const editionsDir = path.join(process.cwd(), 'content/editions');

  if (!fs.existsSync(editionsDir)) notFound();

  const editions = fs
    .readdirSync(editionsDir)
    .filter((dir) =>
      fs.existsSync(path.join(editionsDir, dir, 'index.mdx'))
    )
    .sort()
    .reverse();

  const latest = editions[0];
  if (!latest) notFound();

  const content = fs.readFileSync(
    path.join(editionsDir, latest, 'index.mdx'),
    'utf8'
  );

  return (
    <main style={{ padding: '4rem', maxWidth: '900px', margin: '0 auto' }}>
      <article dangerouslySetInnerHTML={{ __html: content }} />
    </main>
  );
}
