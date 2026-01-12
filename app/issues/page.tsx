import fs from "fs";
import path from "path";

export default function Issues() {
  const dir = path.join(process.cwd(), "content/editions");
  const editions = fs.readdirSync(dir).sort().reverse();

  return (
    <section>
      <h1>Issues</h1>
      <ul>
        {editions.map(e => (
          <li key={e}>
            <a href={`/issues/${e}`}>{e}</a>
          </li>
        ))}
      </ul>
    </section>
  );
}
