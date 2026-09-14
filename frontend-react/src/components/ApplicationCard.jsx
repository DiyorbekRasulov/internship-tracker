import { STATUSES } from "../constants";

// one card, drawn once per application
export default function ApplicationCard({ app, onStatusChange, onDelete }) {
  return (
    <div className="card">
      <span className={`dot ${app.status}`} />

      <div className="info">
        <div className="company">{app.company}</div>
        <div className="role">
          {app.role}
          {/* only show the link when there is one */}
          {app.link && (
            <>
              {" · "}
              <a href={app.link} target="_blank" rel="noreferrer">
                link
              </a>
            </>
          )}
        </div>
      </div>

      <select
        value={app.status}
        onChange={(event) => onStatusChange(app.id, event.target.value)}
      >
        {STATUSES.map((status) => (
          <option key={status} value={status}>
            {status}
          </option>
        ))}
      </select>

      <button className="delete" onClick={() => onDelete(app.id)} title="delete">
        &times;
      </button>
    </div>
  );
}
