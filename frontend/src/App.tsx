
import { useEffect, useState } from "react";
import { fetchTasks, createTask, toggleTaskStatus } from "./api";
import './App.css';

interface Task {
  id: number;
  title: string;
  status: string;
}

function App() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [title, setTitle] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadTasks = async () => {
    try {
      const data = await fetchTasks();
      setTasks(data || []);
      setError(null);
    } catch (e: any) {
      setError("Не удалось загрузить задачи. Проверьте подключение.");
    } finally {
      setLoading(false);
    }
  };

  const addTask = async () => {
    if (!title.trim()) return;
    try {
      await createTask(title);
      setTitle("");
      await loadTasks();
    } catch (e: any) {
      setError("Не удалось создать задачу");
    }
  };

  const toggleTask = async (task: Task) => {
    try {
      await toggleTaskStatus(task.id, task.status);
      await loadTasks();
    } catch (e: any) {
      setError("Не удалось изменить статус задачи");
    }
  };

  useEffect(() => {
    const tg = window.Telegram?.WebApp;

    if (tg) {
      tg.ready();
      tg.expand();
    } else {
      setError("Это приложение работает только внутри Telegram Mini App");
    }

    loadTasks();
  }, []);

  if (loading) {
    return <p style={{ textAlign: 'center', padding: '50px' }}>Загрузка...</p>;
  }

  return (
    <div style={{ padding: 20, maxWidth: '600px', margin: '0 auto' }}>
      <h2>Мои задачи</h2>

      {error && (
        <div style={{
          color: 'red',
          padding: '10px',
          background: '#ffebee',
          borderRadius: '8px',
          marginBottom: '15px'
        }}>
          {error}
        </div>
      )}

      <div style={{ display: 'flex', gap: '10px', marginBottom: '20px' }}>
        <input
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="Новая задача..."
          style={{ flex: 1, padding: '10px', borderRadius: '6px', border: '1px solid #ccc' }}
        />
        <button
          onClick={addTask}
          disabled={!title.trim()}
          style={{
            padding: '10px 20px',
            background: '#4caf50',
            color: 'white',
            border: 'none',
            borderRadius: '6px',
            cursor: title.trim() ? 'pointer' : 'not-allowed'
          }}
        >
          Добавить
        </button>
      </div>

      {tasks.length === 0 ? (
        <p style={{ textAlign: 'center', color: '#777' }}>Задач пока нет</p>
      ) : (
        <ul style={{ listStyle: 'none', padding: 0 }}>
          {tasks.map((t) => (
            <li
              key={t.id}
              style={{
                display: 'flex',
                alignItems: 'center',
                padding: '12px',
                background: '#f9f9f9',
                marginBottom: '8px',
                borderRadius: '8px',
                boxShadow: '0 1px 3px rgba(0,0,0,0.1)'
              }}
            >
              <input
                type="checkbox"
                checked={t.status === "done"}
                onChange={() => toggleTask(t)}
                style={{ marginRight: '12px', transform: 'scale(1.3)' }}
              />
              <span
                style={{
                  flex: 1,
                  textDecoration: t.status === "done" ? 'line-through' : 'none',
                  color: t.status === "done" ? '#888' : '#000'
                }}
              >
                {t.title}
              </span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default App;