import { useState, useEffect } from "react";
import AddForm from "./components/AddForm";
import ApplicationCard from "./components/ApplicationCard";
import * as api from "./api";

export default function App() {
  // when this list changes react redraws the page for us
  const [apps, setApps] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  // the empty array means run this once, when the page first loads
  useEffect(() => {
    refresh();
  }, []);

  async function refresh() {
    try {
      setApps(await api.getApplications());
      setError("");
    } catch {
      setError("cannot reach the api, is flask running on port 5000?");
    } finally {
      setLoading(false);
    }
  }

  async function handleAdd(form) {
    try {
      await api.createApplication(form);
      refresh();
    } catch (err) {
      setError(err.message);
    }
  }

  async function handleStatusChange(id, status) {
    await api.updateApplication(id, { status });
    refresh();
  }

  async function handleDelete(id) {
    if (!confirm("delete this application?")) return;
    await api.deleteApplication(id);
    refresh();
  }

  return (
    <>
      <header>
        <h1>Internship Tracker</h1>
        <p className="summary">
          {loading ? "loading..." : `${apps.length} applications tracked`}
        </p>
      </header>

      <main>
        <AddForm onAdd={handleAdd} />

        {error && <p className="error">{error}</p>}

        {!loading && apps.length === 0 && !error && (
          <p className="empty">nothing yet, add your first application above</p>
        )}

        {/* key lets react tell the cards apart when the list changes */}
        {apps.map((app) => (
          <ApplicationCard
            key={app.id}
            app={app}
            onStatusChange={handleStatusChange}
            onDelete={handleDelete}
          />
        ))}
      </main>
    </>
  );
}
