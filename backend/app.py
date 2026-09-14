from flask import Flask, request
from flask_cors import CORS
from db import get_db, init_db

app = Flask(__name__)
# lets the react app run on a different port and still call this server
CORS(app)

# gunicorn imports this file rather than running it, so the main block below
# never fires in production. this creates the table before the first request.
_schema_ready = False


@app.before_request
def ensure_schema():
    global _schema_ready
    if not _schema_ready:
        init_db()
        _schema_ready = True




@app.route("/api/health")
def health():
    return {"status": "ok"}


# list every application, newest first
@app.route("/api/applications", methods=["GET"])
def list_applications():
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM applications ORDER BY created_at DESC"
    ).fetchall()
    # flask cannot turn sqlite rows into json, so convert each to a dict
    result = [dict(row) for row in rows]
    conn.close()
    return result


# add a new application
@app.route("/api/applications", methods=["POST"])
def create_application():
    # read the json body the client sent
    data = request.get_json(silent=True) or {}

    company = (data.get("company") or "").strip()
    role = (data.get("role") or "").strip()

    # check the input before touching the database
    if not company or not role:
        return {"error": "company and role are required"}, 400

    conn = get_db()
    cursor = conn.execute(
        # the question marks are placeholders, sqlite fills them in safely
        "INSERT INTO applications (company, role, link, status, notes)"
        " VALUES (?, ?, ?, ?, ?)",
        (
            company,
            role,
            data.get("link"),
            data.get("status") or "applied",
            data.get("notes"),
        ),
    )
    # commit saves the change to the file
    conn.commit()
    # read back the row we just made so we can return it
    new_row = conn.execute(
        "SELECT * FROM applications WHERE id = ?", (cursor.lastrowid,)
    ).fetchone()
    conn.close()
    # 201 means created
    return dict(new_row), 201


# change fields on one application
@app.route("/api/applications/<int:app_id>", methods=["PATCH"])
def update_application(app_id):
    data = request.get_json(silent=True) or {}

    conn = get_db()
    row = conn.execute(
        "SELECT * FROM applications WHERE id = ?", (app_id,)
    ).fetchone()
    # nothing to update if that id does not exist
    if row is None:
        conn.close()
        return {"error": "not found"}, 404

    # only these columns may be changed
    allowed = ["company", "role", "link", "status", "notes"]
    # keep only the fields the client actually sent
    updates = {key: data[key] for key in allowed if key in data}
    if not updates:
        conn.close()
        return {"error": "nothing to update"}, 400

    # builds a string like "status = ?, notes = ?"
    assignments = ", ".join(f"{key} = ?" for key in updates)
    conn.execute(
        f"UPDATE applications SET {assignments} WHERE id = ?",
        (*updates.values(), app_id),
    )
    conn.commit()
    updated = conn.execute(
        "SELECT * FROM applications WHERE id = ?", (app_id,)
    ).fetchone()
    conn.close()
    return dict(updated)


# remove one application
@app.route("/api/applications/<int:app_id>", methods=["DELETE"])
def delete_application(app_id):
    conn = get_db()
    cursor = conn.execute("DELETE FROM applications WHERE id = ?", (app_id,))
    conn.commit()
    # rowcount is 0 when no row had that id
    deleted = cursor.rowcount
    conn.close()

    if deleted == 0:
        return {"error": "not found"}, 404
    # 204 means success with nothing to send back
    return "", 204


if __name__ == "__main__":
    # create the table if it is missing, then start the server
    init_db()
    app.run(debug=True, port=5000)
