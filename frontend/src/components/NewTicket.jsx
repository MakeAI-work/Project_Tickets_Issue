import React, { useState } from "react";
import { classifyAnswer } from "../api";
import "../styles/App.css";
import "../styles/badges.css";

export default function NewTicket() {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!text.trim()) return;
    setLoading(true);
    try {
      const res = await classifyAnswer(text);
      setResult(res.data);
      setText("");
    } catch (err) {
      console.error(err);
      alert("Error contacting backend");
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="card new-ticket">
      <h2>Submit New Ticket</h2>
      <form onSubmit={handleSubmit}>
        <textarea
          rows={6}
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Paste ticket text here"
          style={{ width: "100%" }}
        />
        <button className="full-btn" type="submit" disabled={loading}>
          {loading ? "Analyzing..." : "Analyze"}
        </button>
      </form>

      {result && (
        <div className="analysis-container">
          <h3>Internal Analysis</h3>
          <pre>{JSON.stringify(result.analysis, null, 2)}</pre>

          <h3>Final Response</h3>
          <p>{result.response}</p>
          {result.sources?.length > 0 && (
            <ul>
              {result.sources.map((u) => (
                <li key={u}>
                  <a href={u} target="_blank" rel="noreferrer">
                    {u}
                  </a>
                </li>
              ))}
            </ul>
          )}
        </div>
      )}
    </section>
  );
}
