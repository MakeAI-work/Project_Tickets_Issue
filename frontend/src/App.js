import { useEffect, useState } from 'react';
import { fetchTickets } from './api';
import TicketsTable from './components/TicketsTable';
import NewTicket from './components/NewTicket';
import ConnectionStatus from './components/ConnectionStatus';
import './styles/App.css';

function App() {
  const [tickets, setTickets] = useState([]);
  const [filter, setFilter] = useState("all");
  const topics = Array.from(new Set(tickets.map(t=>t.topic))).sort();
  const visible = filter==="all"? tickets : tickets.filter(t=>t.topic===filter);
  const total = visible.length;
  const p0 = tickets.filter(t=>t.priority==="P0").length;
  const p1 = tickets.filter(t=>t.priority==="P1").length;
  const p2 = tickets.filter(t=>t.priority==="P2").length;

  useEffect(() => {
    fetchTickets().then((r) => setTickets(r.data)).catch(console.error);
  }, []);
  return (
    <div className="container">
      <h1>Atlan Helpdesk Demo</h1>
      <ConnectionStatus />
      <div className="filter-section">
        <div className="filter-row">
          <span className="filter-icon">🔍</span>
          <label>Filter by Topic</label>
          <select className="filter-select" value={filter} onChange={e=>setFilter(e.target.value)}>
            <option value="all">All Topics</option>
            {topics.map(tp=> <option key={tp} value={tp}>{tp}</option>)}
          </select>
        </div>
      </div>
      <div className="stats-bar">
        <div className="stat">
          <span className="stat-icon">📊</span>
          <div className="stat-content">
            <span className="stat-number">{total}</span>
            <span className="stat-label">Total Tickets</span>
          </div>
        </div>
        <div className="stat red">
          <span className="stat-icon">🚨</span>
          <div className="stat-content">
            <span className="stat-number">{p0}</span>
            <span className="stat-label">Critical</span>
          </div>
        </div>
        <div className="stat amber">
          <span className="stat-icon">⚠️</span>
          <div className="stat-content">
            <span className="stat-number">{p1}</span>
            <span className="stat-label">High Priority</span>
          </div>
        </div>
        <div className="stat green">
          <span className="stat-icon">✅</span>
          <div className="stat-content">
            <span className="stat-number">{p2}</span>
            <span className="stat-label">Normal</span>
          </div>
        </div>
      </div>
      <div className="grid-two">
        <div className="left-pane card" style={{overflowY:'auto',maxHeight:'75vh'}}>
          <TicketsTable rows={visible} />
        </div>
        <div className="right-pane">
          <NewTicket />
        </div>
      </div>
    </div>
  );
}

export default App;
