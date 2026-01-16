import { useEffect, useState } from "react";

export default function History({ refreshKey }) {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const fetchHistory = async () => {
    setLoading(true);
    setError("");

    try {
      const res = await fetch("http://localhost:5000/api/history?limit=10");

      const data = await res.json().catch(() => ({}));

      if (!res.ok) {
        setError(data.error || "History API failed.");
        setHistory([]);
      } else {
        setHistory(Array.isArray(data.history) ? data.history : []);
      }
    } catch (err) {
      setError("Backend not reachable. Start Flask on port 5000.");
      setHistory([]);
    }

    setLoading(false);
  };

  useEffect(() => {
    fetchHistory();
  }, [refreshKey]);

  return (
    <div style={{ marginTop: 30 }}>
      <h2>Recent Checks</h2>

      {loading && <p>Loading history...</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}

      {!loading && !error && history.length === 0 && <p>No history yet.</p>}

      {history.map((item) => (
        <div
          key={item.id}
          style={{
            padding: 12,
            border: "1px solid #ccc",
            borderRadius: 8,
            marginTop: 10,
          }}
        >
          <p style={{ margin: 0 }}>
            <b>{item.prediction}</b> | Confidence: {item.confidence}
          </p>

          <p style={{ margin: "6px 0" }}>
            {item.input_text}
          </p>

          <small>{item.created_at}</small>
        </div>
      ))}
    </div>
  );
}
