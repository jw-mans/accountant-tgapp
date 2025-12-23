import { useEffect, useState } from "react";
import { fetchTasks, createTask, toggleTaskStatus } from "./api";

interface Task {
  id: number;
  title: string;
  status: string;
}

function App() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [title, setTitle] = useState("");
  const [loading, setLoading] = useState(true);

  const loadTasks = async () => {
    try {
      const data = await fetchTasks();
      setTasks(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const addTask = async () => {
    if (!title.trim()) return;
    try {
      await createTask(title);
      setTitle("");
      loadTasks();
    } catch (e) {
      console.error(e);
    }
  };

  const toggleTask = async (task: Task) => {
    try {
      await toggleTaskStatus(task.id, task.status);
      loadTasks();
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    if (window.Telegram?.WebApp) {
      const tg = window.Telegram.WebApp;
      tg.ready();
      tg.expand();
    } else {
      // Для теста в браузере без Telegram
      window.Telegram = { WebApp: { initData: "dummy", ready: () => {}, expand: () => {} } };
    }
    loadTasks();
  }, []);

  if (loading) return <p>Loading...</p>;

  return (
    <div style={{ padding: 20 }}>
      <h3>Tasks</h3>
      <input
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        placeholder="New task"
      />
      <button onClick={addTask} style={{ marginLeft: 5 }}>Add</button>

      <ul>
        {tasks.map((t) => (
          <li key={t.id} style={{ marginTop: 5 }}>
            <input
              type="checkbox"
              checked={t.status === "done"}
              onChange={() => toggleTask(t)}
            />
            <span style={{ marginLeft: 8 }}>{t.title}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
