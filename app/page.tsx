import fs from "fs";
import path from "path";
import { marked } from "marked";
import CoverHero from "@/app/components/CoverHero";

export default function Home() {
  const editionsDir = path.join(process.cwd(), "content/editions");
  const editions = fs.readdirSync(editionsDir).sort().reverse();
  const latest = editions[0];

  const meta = JSON.parse(
    fs.readFileSync(path.join(editionsDir, latest, "meta.json"), "utf8")
  );
  const raw = fs.readFileSync(
    path.join(editionsDir, latest, "index.mdx"),
    "utf8"
  );

  return (
    <>
      <CoverHero title={meta.title} />
      <article dangerouslySetInnerHTML={{ __html: marked(raw) }} />
    </>
  );
}
