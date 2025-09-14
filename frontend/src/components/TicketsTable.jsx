import React from "react";
import "../styles/App.css";
import "../styles/badges.css";

export default function TicketsTable({ rows }) {
  if (!rows?.length) return <p>No tickets found.</p>;

  return (
    <div className="card-list">
      {rows.map((t) => (
        <div key={t.id} className="ticket-card">
          <div className="ticket-header">
            <span className="ticket-id">{t.id}</span>
            <span className={`badge ${t.priority}`}>{t.priority}</span>
          </div>
          <h3 className="ticket-subject">{t.subject}</h3>
          <div className="ticket-meta">
            <span className="chip">{t.topic}</span>
            <span className="chip soft">{t.sentiment}</span>
          </div>
        </div>
      ))}
    </div>
  );
}
