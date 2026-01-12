import fs from "fs";
import path from "path";
import Link from "next/link";

export default function EditionsIndex() {
  const editionsDir = path.join(process.cwd(), "content/editions");
  const slugs = fs.readdirSync(editionsDir);

  return (
    <main style={{ padding: "4rem" }}>
      <h1>Archived Editions</h1>
      <ul>
        {slugs.map(slug => (
          <li key={slug}>
            <Link href={`/editions/${slug}`}>{slug}</Link>
          </li>
        ))}
      </ul>
    </main>
  );
}
