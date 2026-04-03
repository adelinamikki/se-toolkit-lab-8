---
name: observability
description: Use observability MCP tools to investigate logs, errors, and traces
always: true
---

# Observability skill

This skill teaches the agent how to use observability MCP tools to investigate
system health, errors, and request traces.

## Available tools

- `logs_search`: Search structured logs in VictoriaLogs using a LogsQL query.
  Use `_time:<window>` for time filtering (e.g. `_time:10m`, `_time:1h`),
  `service.name:"ServiceName"` for service, `severity:ERROR` for errors.
- `logs_error_count`: Count errors per service over a time window in VictoriaLogs.
  Returns a summary of error counts grouped by service name.
- `traces_list`: List recent traces from VictoriaTraces. Optionally filter by service name.
  Returns trace IDs, span counts, and durations.
- `traces_get`: Fetch a specific trace by ID from VictoriaTraces and show the span hierarchy.
  Use the trace_id from log entries or traces_list output.

## Strategy

- **When the user asks about errors or system health:**
  1. First call `logs_error_count` to get a quick overview of recent errors per service.
  2. If errors are found, use `logs_search` to drill into the specific service and time window.
     For example: `_time:10m service.name:"Learning Management Service" severity:ERROR`
  3. If a `trace_id` appears in the log results, call `traces_get` with that ID to inspect
     the full request path and pinpoint where the failure occurred.

- **When the user asks about a specific request or trace:**
  1. If they provide a trace ID, call `traces_get` directly.
  2. If they don't, use `logs_search` to find the relevant request logs and extract the trace ID.
  3. Then call `traces_get` with that trace ID.

- **When the user asks about recent activity for a service:**
  1. Call `traces_list` with the service name to see recent traces.
  2. Summarize the results — span counts, durations, any errors.

## Formatting

- **Never dump raw JSON.** Summarize findings in plain language.
- When reporting errors, include:
  - Which service is affected
  - What the error message says
  - When it happened (timestamp)
  - The trace ID if available
- When reporting trace data, show:
  - The service hierarchy (which services handled the request)
  - Where the error occurred in the span tree
  - Duration of each step

## Time scoping

- Always scope queries to a narrow, relevant time window.
- Prefer `_time:10m` for recent troubleshooting, `_time:1h` for broader checks.
- If the user asks about "the last hour" or similar, use that window directly.
- When checking for fresh errors, use `_time:10m` to avoid unrelated historical noise.

## Examples

- **"Any errors in the last 10 minutes?"**
  1. `logs_error_count` with `time_window=10m`
  2. If errors found, `logs_search` with `_time:10m severity:ERROR`
  3. If trace IDs found, `traces_get` for the most recent one
  4. Summarize: which services had errors, what they were, and the trace path

- **"Any LMS backend errors in the last 10 minutes?"**
  1. `logs_error_count` with `time_window=10m, service="Learning Management Service"`
  2. If errors found, `logs_search` with `_time:10m service.name:"Learning Management Service" severity:ERROR`
  3. Extract any trace_id from the logs and call `traces_get`
  4. Summarize the failure path concisely

- **"Show me the trace for request XYZ"**
  1. If a trace ID is given, call `traces_get` directly
  2. If not, use `logs_search` to find the request and extract the trace ID
  3. Call `traces_get` and show the span hierarchy

- **"What can you do?"**
  Explain that you can search structured logs, count errors per service, list recent traces,
  and inspect individual request traces to diagnose failures across services.
