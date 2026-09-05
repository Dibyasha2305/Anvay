import { useState } from "react"
import "./App.css"

const API_URL =
  import.meta.env.VITE_API_URL ||
  "http://127.0.0.1:9000"

function App() {
  const [backendFile, setBackendFile] = useState(null)
  const [aiFile, setAiFile] = useState(null)

  const [report, setReport] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")

  const [jobStep, setJobStep] = useState("")
  const [jobMessage, setJobMessage] = useState("")

  async function handleAnalyze() {
    if (!backendFile || !aiFile) {
      setError("Select both services before running Anvay.")
      return
    }

    setLoading(true)
    setError("")
    setReport(null)

    setJobStep("starting")
    setJobMessage("Starting Anvay engine")

    const formData = new FormData()

    formData.append("backend_file", backendFile)
    formData.append("ai_file", aiFile)

    try {
      // Start analysis job
      const response = await fetch(
          `${API_URL}/analyze`,
        {
          method: "POST",
          body: formData
        }
      )

      const startData = await response.json()

      if (!response.ok) {
        throw new Error(
          startData.message || "Could not start Anvay."
        )
      }

      const jobId = startData.job_id

      // Poll job status
      const pollStatus = async () => {
        try {
          const statusResponse = await fetch(
            `http://127.0.0.1:9000/status/${jobId}`
          )

          const statusData = await statusResponse.json()

          if (!statusResponse.ok) {
            throw new Error(
              statusData.message ||
              "Could not read analysis status."
            )
          }

          setJobStep(statusData.step)
          setJobMessage(statusData.message || "")

          // Job failed
          if (statusData.step === "failed") {
            setLoading(false)

            throw new Error(
              statusData.message ||
              "Integration failed."
            )
          }

          // Job completed
          if (statusData.step === "complete") {
            setReport(statusData.result)
            setLoading(false)
            return
          }

          // Continue polling
          setTimeout(pollStatus, 700)

        } catch (err) {
          setError(
            err.message ||
            "Something went wrong while checking progress."
          )

          setLoading(false)
        }
      }

      await pollStatus()

    } catch (err) {
      setError(
        err.message ||
        "Could not connect to Anvay."
      )

      setLoading(false)
    }
  }

  const verified =
    report?.verification?.success === true

  const isAnalyzing =
    jobStep === "starting" ||
    jobStep === "analyzing"

  const isIntegrating =
    jobStep === "integrating" ||
    jobStep === "verifying" ||
    jobStep === "packaging" ||
    jobStep === "complete"

  const isVerifying =
    jobStep === "verifying" ||
    jobStep === "packaging" ||
    jobStep === "complete"

  const isPackaging =
    jobStep === "packaging" ||
    jobStep === "complete"

  return (
    <div className="app">

      <div className="grid-bg" />

      {/* HEADER */}

      <header className="topbar">

        <div className="wordmark">
          ANVAY<span>.</span>
        </div>

        <div className="topbar-right">
          <span className="live-dot" />
          LOCAL ENGINE
        </div>

      </header>


      {/* MAIN */}

      <main className="shell">

        {/* HERO */}

        <section className="hero">

          <div className="eyebrow">
            CODE INTEGRATION / 01
          </div>

          <h1>
            Integrate the things
            <br />
            your code wasn't built
            <br />
            to talk to.
          </h1>

          <p className="hero-copy">
            Analyze two services. Detect the contract gap.
            Generate the bridge. Verify the result.
          </p>

        </section>


        {/* INPUT WORKSPACE */}

        <section className="workspace">

          <div className="workspace-head">

            <div>
              <div className="mini-label">
                INPUTS
              </div>

              <h2>
                Drop your services.
              </h2>
            </div>

            <div className="step-count">
              01 / 03
            </div>

          </div>


          <div className="upload-grid">

            {/* BACKEND */}

            <label className="dropzone">

              <input
                type="file"
                accept=".py"
                onChange={(event) => {
                  const file =
                    event.target.files?.[0] || null

                  setBackendFile(file)
                  setError("")
                }}
              />

              <div className="dropzone-top">

                <span className="service-number">
                  01
                </span>

                <span className="service-tag">
                  BACKEND
                </span>

              </div>

              <div className="drop-icon">
                ↗
              </div>

              <div className="drop-title">
                {backendFile
                  ? backendFile.name
                  : "Choose backend"}
              </div>

              <div className="drop-description">
                Python / FastAPI service
              </div>

              <div className="drop-footer">
                {backendFile
                  ? "FILE READY"
                  : "SELECT FILE"}
              </div>

            </label>


            {/* AI SERVICE */}

            <label className="dropzone">

              <input
                type="file"
                accept=".py"
                onChange={(event) => {
                  const file =
                    event.target.files?.[0] || null

                  setAiFile(file)
                  setError("")
                }}
              />

              <div className="dropzone-top">

                <span className="service-number">
                  02
                </span>

                <span className="service-tag">
                  AI SERVICE
                </span>

              </div>

              <div className="drop-icon">
                ✦
              </div>

              <div className="drop-title">
                {aiFile
                  ? aiFile.name
                  : "Choose AI service"}
              </div>

              <div className="drop-description">
                Model / inference endpoint
              </div>

              <div className="drop-footer">
                {aiFile
                  ? "FILE READY"
                  : "SELECT FILE"}
              </div>

            </label>

          </div>


          {/* RUN */}

          <div className="run-row">

            <button
              className="run-button"
              onClick={handleAnalyze}
              disabled={loading}
            >

              <span>
                {loading
                  ? "RUNNING ANVAY"
                  : "RUN ANVAY"}
              </span>

              <span className="run-arrow">
                →
              </span>

            </button>

          </div>


          {/* LIVE PROGRESS */}

          {loading && (

            <div className="anvay-progress">

              <div className="progress-title">
                ANVAY ENGINE
              </div>

              <div className="progress-list">

                {/* ANALYZE */}

                <div
                  className={
                    isAnalyzing
                      ? "progress-item active"
                      : "progress-item done"
                  }
                >

                  <span>01</span>

                  <strong>
                    {isAnalyzing ? "ANALYZING" : "ANALYZED"}
                  </strong>

                  <small>
                    {isAnalyzing
                      ? jobMessage
                      : "Contracts detected"}
                  </small>

                </div>


                {/* INTEGRATE */}

                <div
                  className={
                    jobStep === "integrating"
                      ? "progress-item active"
                      : isIntegrating
                      ? "progress-item done"
                      : "progress-item"
                  }
                >

                  <span>02</span>

                  <strong>
                    {jobStep === "integrating"
                      ? "INTEGRATING"
                      : isIntegrating
                      ? "INTEGRATED"
                      : "INTEGRATING"}
                  </strong>

                  <small>
                    {jobStep === "integrating"
                      ? jobMessage
                      : "Generating adapter"}
                  </small>

                </div>


                {/* VERIFY */}

                <div
                  className={
                    jobStep === "verifying"
                      ? "progress-item active"
                      : isVerifying
                      ? "progress-item done"
                      : "progress-item"
                  }
                >

                  <span>03</span>

                  <strong>
                    {jobStep === "verifying"
                      ? "VERIFYING"
                      : isVerifying
                      ? "VERIFIED"
                      : "VERIFYING"}
                  </strong>

                  <small>
                    {jobStep === "verifying"
                      ? jobMessage
                      : "Docker end-to-end test"}
                  </small>

                </div>


                {/* PACKAGE */}

                <div
                  className={
                    jobStep === "packaging"
                      ? "progress-item active"
                      : isPackaging
                      ? "progress-item done"
                      : "progress-item"
                  }
                >

                  <span>04</span>

                  <strong>
                    {jobStep === "packaging"
                      ? "PACKAGING"
                      : isPackaging
                      ? "READY"
                      : "PACKAGING"}
                  </strong>

                  <small>
                    {jobStep === "packaging"
                      ? jobMessage
                      : "Preparing project ZIP"}
                  </small>

                </div>

              </div>

            </div>

          )}

        </section>


        {/* ERROR */}

        {error && (

          <section className="error-panel">

            <span className="error-mark">
              !
            </span>

            <div>

              <strong>
                ANVAY STOPPED
              </strong>

              <p>
                {error}
              </p>

            </div>

          </section>

        )}


        {/* RESULT */}

        {report && (

          <section className="results">

            {/* STATUS */}

            <div
              className={
                verified
                  ? "result-status verified"
                  : "result-status failed"
              }
            >

              <div className="status-left">

                <div className="status-symbol">
                  {verified ? "✓" : "!"}
                </div>

                <div>

                  <div className="status-kicker">
                    INTEGRATION STATUS
                  </div>

                  <div className="status-title">
                    {verified
                      ? "VERIFIED"
                      : "FAILED"}
                  </div>

                </div>

              </div>

              <div className="status-message">
                {report.verification?.message}
              </div>

            </div>


            {/* SYSTEM MAP */}

            <div className="result-heading">

              <div className="mini-label">
                SYSTEM MAP
              </div>

              <h2>
                What Anvay connected
              </h2>

            </div>


            <div className="pipeline">

              <div className="pipeline-node">

                <div className="node-index">
                  01
                </div>

                <div className="node-type">
                  BACKEND
                </div>

                <div className="node-endpoint">
                  {report.backend.method}{" "}
                  {report.backend.path}
                </div>

              </div>


              <div className="pipeline-bridge">

                <div className="bridge-line" />

                <div className="bridge-box">
                  <span>ANVAY</span>
                  <small>ADAPTER</small>
                </div>

                <div className="bridge-line" />

              </div>


              <div className="pipeline-node">

                <div className="node-index">
                  02
                </div>

                <div className="node-type">
                  AI SERVICE
                </div>

                <div className="node-endpoint">
                  {report.ai_service.method}{" "}
                  {report.ai_service.path}
                </div>

              </div>

            </div>


            {/* CONTRACTS */}

            <div className="data-grid">

              {/* BACKEND CONTRACT */}

              <div className="data-panel">

                <div className="panel-head">

                  <span>
                    BACKEND CONTRACT
                  </span>

                  <span>
                    {report.backend.path}
                  </span>

                </div>


                <div className="contract-section">

                  <div className="contract-label">
                    REQUEST
                  </div>

                  {Object.entries(
                    report.backend.request || {}
                  ).map(([key, value]) => (

                    <div
                      className="field-row"
                      key={key}
                    >

                      <code>
                        {key}
                      </code>

                      <span>
                        {value}
                      </span>

                    </div>

                  ))}

                </div>


                <div className="contract-section">

                  <div className="contract-label">
                    RESPONSE
                  </div>

                  {Object.entries(
                    report.backend.response || {}
                  ).map(([key, value]) => (

                    <div
                      className="field-row"
                      key={key}
                    >

                      <code>
                        {key}
                      </code>

                      <span>
                        {value}
                      </span>

                    </div>

                  ))}

                </div>

              </div>


              {/* AI CONTRACT */}

              <div className="data-panel">

                <div className="panel-head">

                  <span>
                    AI CONTRACT
                  </span>

                  <span>
                    {report.ai_service.path}
                  </span>

                </div>


                <div className="contract-section">

                  <div className="contract-label">
                    REQUEST
                  </div>

                  {Object.entries(
                    report.ai_service.request || {}
                  ).map(([key, value]) => (

                    <div
                      className="field-row"
                      key={key}
                    >

                      <code>
                        {key}
                      </code>

                      <span>
                        {value}
                      </span>

                    </div>

                  ))}

                </div>


                <div className="contract-section">

                  <div className="contract-label">
                    RESPONSE
                  </div>

                  {Object.entries(
                    report.ai_service.response || {}
                  ).map(([key, value]) => (

                    <div
                      className="field-row"
                      key={key}
                    >

                      <code>
                        {key}
                      </code>

                      <span>
                        {value}
                      </span>

                    </div>

                  ))}

                </div>

              </div>

            </div>


            {/* MAPPINGS */}

            <div className="result-heading compact">

              <div className="mini-label">
                CONTRACT TRANSLATION
              </div>

              <h2>
                Generated mappings
              </h2>

            </div>


            <div className="mapping-list">

              {(report.mappings || []).map(
                (mapping, index) => (

                  <div
                    className="mapping-item"
                    key={index}
                  >

                    <span className="mapping-source">
                      {mapping.backend}
                    </span>

                    <span className="mapping-arrow">
                      →
                    </span>

                    <span className="mapping-target">
                      {mapping.ai_service}
                    </span>

                  </div>

                )
              )}

            </div>


            {/* MISMATCH */}

            <div className="result-heading compact">

              <div className="mini-label">
                DETECTED DIFFERENCES
              </div>

              <h2>
                Mismatches
              </h2>

            </div>


            <div className="mismatch-panel">

              {!report.mismatches ||
              report.mismatches.length === 0 ? (

                <div className="clean-state">
                  <span>✓</span>
                  No mismatches detected
                </div>

              ) : (

                report.mismatches.map(
                  (mismatch, index) => (

                    <div
                      className="mismatch-item"
                      key={index}
                    >

                      <span className="mismatch-icon">
                        !
                      </span>

                      <div>

                        <strong>
                          {mismatch.type}
                        </strong>

                        <p>
                          {mismatch.backend}
                          {" → "}
                          {mismatch.ai_service}
                        </p>

                      </div>

                    </div>

                  )
                )

              )}

            </div>


            {/* VERIFICATION */}

            <div className="result-heading compact">

              <div className="mini-label">
                RUNTIME CHECK
              </div>

              <h2>
                Verification
              </h2>

            </div>


            <div className="verification-grid">

              <div className="verify-cell">
                <span>DOCKER BUILD</span>
                <strong>
                  {verified ? "PASS" : "FAIL"}
                </strong>
              </div>

              <div className="verify-cell">
                <span>BACKEND</span>
                <strong>
                  {verified ? "PASS" : "FAIL"}
                </strong>
              </div>

              <div className="verify-cell">
                <span>AI SERVICE</span>
                <strong>
                  {verified ? "PASS" : "FAIL"}
                </strong>
              </div>

              <div className="verify-cell">
                <span>E2E REQUEST</span>
                <strong>
                  {verified ? "PASS" : "FAIL"}
                </strong>
              </div>

            </div>


            {/* TEST RESPONSE */}

            {report.verification?.response && (

              <div className="test-response">

                <div className="contract-label">
                  TEST RESPONSE
                </div>

                <pre>
{JSON.stringify(
  report.verification.response,
  null,
  2
)}
                </pre>

              </div>

            )}


            {/* DOWNLOAD */}

            {report.download_available && (

              <div className="download-panel">

                <div>

                  <div className="download-kicker">
                    VERIFIED ARTIFACT
                  </div>

                  <h3>
                    Your integration is ready.
                  </h3>

                  <p>
                    Anvay built and verified the
                    complete project.
                  </p>

                </div>

                <a
                  href={`${API_URL}/download`}
                  className="download-button"
                  download
                >
                  DOWNLOAD ZIP
                  <span>↓</span>
                </a>

              </div>

            )}

          </section>

        )}

      </main>


      {/* FOOTER */}

      <footer className="footer">

        <span>
          ANVAY / INTEGRATION ENGINE
        </span>

        <span>
          BUILD 01
        </span>

      </footer>

    </div>
  )
}

export default App