import { useState } from "react"
import "./App.css"

const API_URL = import.meta.env.VITE_API_URL

function App() {
  const [question, setQuestion] = useState("")
  const [answer, setAnswer] = useState("")
  const [loading, setLoading] = useState(false)
  const [agentsUsed, setAgentsUsed] = useState<string[]>([])

  async function handleAsk() {
    if (!question.trim()) {
      return
    }

    setLoading(true)
    setAnswer("")
    setAgentsUsed([])

    try {
      const response = await fetch(`${API_URL}/ask`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question: question,
        }),
      })

      if (!response.ok) {
        throw new Error("Request failed")
      }

      const data = await response.json()
      setAnswer(data.answer)
      setAgentsUsed(data.agents_used)

    } catch (error) {
      setAnswer("Something went wrong. Please try again.")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <header className="topbar">
        <div className="header-meta">
          <span className="eyebrow">ENTERPRISE AI PLATFORM</span>

          <span className="status">
            <span className="status-dot"></span>
            System online
          </span>
        </div>

        <h1>Enterprise AI Data Assistant</h1>

        <p>
          Unified access to enterprise documents and structured data through
          coordinated AI agents.
        </p>
      </header>

      <main className="container">
        <section className="agent-row">
          <div className="agent-card">
            <span className="agent-label">Manager</span>
            <strong>Orchestrator</strong>
            <p>Routes each request to the appropriate specialist.</p>
          </div>

          <div className="agent-card">
            <span className="agent-label">RAG Agent</span>
            <strong>Documents</strong>
            <p>Answers policy, warranty, and knowledge-base questions.</p>
          </div>

          <div className="agent-card">
            <span className="agent-label">SQL Agent</span>
            <strong>Structured Data</strong>
            <p>Answers counts, statuses, and database-driven questions.</p>
          </div>
        </section>

        <section className="workspace">
          <div className="workspace-header">
            <h2>Ask enterprise data</h2>

            <p>
              The manager agent will decide which data source and specialist
              agent to use.
            </p>
          </div>

          <textarea
            placeholder="Example: How many support tickets are there and what does the Acme warranty cover?"
            value={question}
            onChange={(event) => setQuestion(event.target.value)}
            rows={5}
          />

          <div className="actions">
            <span className="helper-text">
              Ask a document, database, or hybrid question
            </span>

            <button onClick={handleAsk} disabled={loading}>
              {loading ? "Processing..." : "Ask Assistant"}
            </button>
          </div>
        </section>

        <section className="suggestions">
          <span className="suggestion-title">Suggested prompts</span>

          <div className="suggestion-buttons">
            <button
              onClick={() =>
                setQuestion("What does the Acme warranty cover?")
              }
            >
              Warranty policy
            </button>

            <button
              onClick={() =>
                setQuestion("How many support tickets are there?")
              }
            >
              Support ticket count
            </button>

            <button
              onClick={() =>
                setQuestion(
                  "How many support tickets are there and what does the Acme warranty cover?"
                )
              }
            >
              Hybrid agent query
            </button>
          </div>
        </section>

        {answer && (
          <section className="answer-card">
            <div className="answer-header">
              <span>AI RESPONSE</span>

              <span className="response-badge">
                {agentsUsed.includes("rag_agent") && agentsUsed.includes("sql_agent")
                  ? "RAG + SQL"
                  : agentsUsed.includes("rag_agent")
                  ? "RAG Agent"
                  : agentsUsed.includes("sql_agent")
                  ? "SQL Agent"
                  : "Manager Agent"}
              </span>
            </div>

            <div className="answer-content">
              {answer}
            </div>
          </section>
        )}

        <section className="architecture">
          <div>
            <span className="architecture-label">Architecture</span>

            <p>
              React + TypeScript → FastAPI → Manager Agent → RAG / SQL Agents
            </p>
          </div>

          <div className="tech-stack">
            <span>React</span>
            <span>FastAPI</span>
            <span>Azure AI Foundry</span>
            <span>Azure AI Search</span>
          </div>
        </section>
      </main>
    </div>
  )
}

export default App