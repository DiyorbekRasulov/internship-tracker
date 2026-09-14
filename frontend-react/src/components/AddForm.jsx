import { useState } from "react";
import { STATUSES } from "../constants";

// what the form looks like when empty
const EMPTY = { company: "", role: "", link: "", status: "applied" };

export default function AddForm({ onAdd }) {
  // one piece of state holds every field
  const [form, setForm] = useState(EMPTY);
  const [saving, setSaving] = useState(false);

  // runs on every keystroke and updates only the field that changed
  function handleChange(event) {
    const { name, value } = event.target;
    setForm((current) => ({ ...current, [name]: value }));
  }

  async function handleSubmit(event) {
    // stop the browser reloading the page
    event.preventDefault();
    setSaving(true);
    try {
      await onAdd(form);
      // clear the inputs only after it saved
      setForm(EMPTY);
    } finally {
      setSaving(false);
    }
  }

  return (
    <form className="add-form" onSubmit={handleSubmit}>
      <input
        name="company"
        placeholder="Company"
        value={form.company}
        onChange={handleChange}
        required
      />
      <input
        name="role"
        placeholder="Role"
        value={form.role}
        onChange={handleChange}
        required
      />
      <input
        name="link"
        type="url"
        placeholder="Link (optional)"
        value={form.link}
        onChange={handleChange}
      />
      <select name="status" value={form.status} onChange={handleChange}>
        {STATUSES.map((status) => (
          <option key={status} value={status}>
            {status}
          </option>
        ))}
      </select>
      <button type="submit" disabled={saving}>
        {saving ? "Saving..." : "Add"}
      </button>
    </form>
  );
}
