// where the flask server is listening
const API = "http://localhost:5000/api";

const listEl = document.getElementById("list");
const formEl = document.getElementById("add-form");
const summaryEl = document.getElementById("summary");

const STATUSES = ["applied", "interviewing", "offer", "rejected"];

// turns text into something safe to drop into html
function escapeHtml(text) {
  const div = document.createElement("div");
  div.textContent = text ?? "";
  return div.innerHTML;
}

// ask the api for every application and draw them
async function loadApplications() {
  const response = await fetch(`${API}/applications`);
  const apps = await response.json();
  render(apps);
}

function render(apps) {
  summaryEl.textContent = `${apps.length} applications tracked`;

  if (apps.length === 0) {
    listEl.innerHTML = `<p class="empty">nothing yet, add your first application above</p>`;
    return;
  }

  // build one card per application
  listEl.innerHTML = apps.map(app => {
    // only show the link if there is one
    const link = app.link
      ? ` &middot; <a href="${escapeHtml(app.link)}" target="_blank">link</a>`
      : "";

    // build the dropdown and mark the current status as selected
    const options = STATUSES.map(s =>
      `<option value="${s}" ${s === app.status ? "selected" : ""}>${s}</option>`
    ).join("");

    return `
      <div class="card">
        <span class="dot ${escapeHtml(app.status)}"></span>
        <div class="info">
          <div class="company">${escapeHtml(app.company)}</div>
          <div class="role">${escapeHtml(app.role)}${link}</div>
        </div>
        <select data-id="${app.id}" class="status-select">${options}</select>
        <button class="delete" data-id="${app.id}" title="delete">&times;</button>
      </div>`;
  }).join("");
}

// handle the add form
formEl.addEventListener("submit", async (event) => {
  // stop the browser reloading the page
  event.preventDefault();

  const body = {
    company: document.getElementById("company").value,
    role: document.getElementById("role").value,
    link: document.getElementById("link").value,
    status: document.getElementById("status").value,
  };

  const response = await fetch(`${API}/applications`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });

  if (!response.ok) {
    const error = await response.json();
    alert(error.error || "could not save");
    return;
  }

  formEl.reset();
  loadApplications();
});

// one listener on the container handles every card inside it
listEl.addEventListener("change", async (event) => {
  if (!event.target.classList.contains("status-select")) return;

  await fetch(`${API}/applications/${event.target.dataset.id}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ status: event.target.value }),
  });
  loadApplications();
});

listEl.addEventListener("click", async (event) => {
  if (!event.target.classList.contains("delete")) return;
  if (!confirm("delete this application?")) return;

  await fetch(`${API}/applications/${event.target.dataset.id}`, {
    method: "DELETE",
  });
  loadApplications();
});

// draw everything as soon as the page opens
loadApplications();
