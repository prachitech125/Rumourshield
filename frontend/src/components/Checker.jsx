import { useState } from "react";

export default function Checker({ onNewCheck }) {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleCheck = async () => {
    setError("");
    setResult(null);

    if (!text.trim()) {
      setError("Please enter some text.");
      return;
    }

    setLoading(true);

    try {
      const res = await fetch("http://127.0.0.1:5000/api/check", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text }),
      });

      const data = await res.json();

      if (!res.ok) {
        setError(data.error || "Something went wrong.");
      } else {
        setResult(data);
        // refresh history after new check
        if (onNewCheck) onNewCheck();
      }
    } catch {
      setError("Backend not running. Start Flask server first.");
    }

    setLoading(false);
  };

  return (
    <div style={{ marginTop: 20 }}>
      <h2>Check a Rumour</h2>

      <textarea
        rows={6}
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Paste social post / news / blog text here..."
        style={{
          width: "100%",
          padding: 12,
          fontSize: 16,
          borderRadius: 8,
        }}
      />

      <button
        onClick={handleCheck}
        disabled={loading}
        style={{
          marginTop: 10,
          padding: "10px 16px",
          cursor: "pointer",
          borderRadius: 8,
        }}
      >
        {loading ? "Checking..." : "Check"}
      </button>

      {error && <p style={{ color: "red", marginTop: 10 }}>{error}</p>}

      {result && (
        <div
          style={{
            marginTop: 20,
            padding: 12,
            border: "1px solid #ccc",
            borderRadius: 8,
          }}
        >
          <h3>Result</h3>
          <p>
            <b>Prediction:</b> {result.prediction}
          </p>
          <p>
            <b>Confidence:</b> {result.confidence}
          </p>

          {result.keywords && result.keywords.length > 0 && (
            <p>
              <b>Matched Keywords:</b> {result.keywords.join(", ")}
            </p>
          )}

          <h4>Fact-check Sources</h4>
          {result.factchecks && result.factchecks.length > 0 ? (
            <ul>
              {result.factchecks.map((fc, index) => (
                <li key={index}>
                  <b>{fc.publisher}</b> — {fc.rating}{" "}
                  <br />
                  <a href={fc.url} target="_blank" rel="noreferrer">
                    Open Source
                  </a>
                </li>
              ))}
            </ul>
          ) : (
            <p>No verified fact-check sources found.</p>
          )}
        </div>
      )}
    </div>
  );
}
