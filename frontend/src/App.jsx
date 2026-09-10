import { useEffect, useState } from "react";

const API = "/api";
const STATUSES = ["todo", "shooting", "done"];

export default function App() {
  const [shots, setShots] = useState([]);
  const [title, setTitle] = useState("");
  const [error, setError] = useState(null);
  const [health, setHealth] = useState("checking");

  async function load() {
    try {
      const r = await fetch(`${API}/shots`);
      if (!r.ok) throw new Error(`GET /shots -> ${r.status}`);
      setShots(await r.json());
      setError(null);
    } catch (e) {
      setError(e.message);
    }
  }

  useEffect(() => {
    load();
    fetch(`${API}/health`)
      .then((r) => (r.ok ? "ok" : `api ${r.status}`))
      .catch(() => "unreachable")
      .then(setHealth);
  }, []);

  async function addShot(e) {
    e.preventDefault();
    if (!title.trim()) return;
    const r = await fetch(`${API}/shots`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title }),
    });
    if (r.ok) {
      setTitle("");
      load();
    } else {
      setError(`POST /shots -> ${r.status}`);
    }
  }

  async function setStatus(id, status) {
    await fetch(`${API}/shots/${id}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ status }),
    });
    load();
  }

  async function remove(id) {
    await fetch(`${API}/shots/${id}`, { method: "DELETE" });
    load();
  }

  return (
    <main>
      <header>
        <h1>ShotList</h1>
        <span className={`health ${health}`}>api: {health}</span>
      </header>

      <form onSubmit={addShot}>
        <input
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="New shot, e.g. golden hour at the pier"
        />
        <button type="submit">Add shot</button>
      </form>

      {error && <p className="error">{error}</p>}
      {!error && shots.length === 0 && <p className="empty">No shots yet. Add the first one above.</p>}

      <ul>
        {shots.map((s) => (
          <li key={s.id} className={s.status}>
            <span className="title">{s.title}</span>
            <select value={s.status} onChange={(e) => setStatus(s.id, e.target.value)}>
              {STATUSES.map((st) => (
                <option key={st}>{st}</option>
              ))}
            </select>
            <button onClick={() => remove(s.id)} aria-label={`delete ${s.title}`}>×</button>
          </li>
        ))}
      </ul>
    </main>
  );
}
