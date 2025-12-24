const API = "/api";

export function authHeaders() {
  return {
    "Content-Type": "application/json",
    "Authorization": "tma " + (window.Telegram?.WebApp?.initData || "")
  };
}

export async function fetchTasks() {
  const res = await fetch(`${API}/tasks`, { headers: authHeaders() });
  if (!res.ok) throw new Error("Failed to fetch tasks");
  return res.json();
}

export async function createTask(title: string) {
  const res = await fetch(`${API}/tasks`, {
    method: "POST",
    headers: authHeaders(),
    body: JSON.stringify({ title }),
  });
  if (!res.ok) throw new Error("Failed to create task");
}

export async function toggleTaskStatus(id: number, currentStatus: string) {
  const res = await fetch(`${API}/tasks/${id}`, {
    method: "PATCH",
    headers: authHeaders(),
    body: JSON.stringify({
      status: currentStatus === "open" ? "done" : "open"
    }),
  });
  if (!res.ok) throw new Error("Failed to update task");
}