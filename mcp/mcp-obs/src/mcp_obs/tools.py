"""Tool schemas, handlers, and registry for the MCP observability server."""

from __future__ import annotations

from collections.abc import Awaitable, Callable, Sequence
from dataclasses import dataclass

from mcp.types import Tool
from pydantic import BaseModel, Field

from mcp_obs.observability import VictoriaLogsClient, VictoriaTracesClient


class LogSearchQuery(BaseModel):
    query: str = Field(
        description=(
            "LogsQL query string. Examples:\n"
            '- `_time:10m service.name:"Learning Management Service"`\n'
            '- `_time:1h severity:ERROR`\n'
            '- `_time:10m service.name:"Learning Management Service" severity:ERROR`\n'
            "Use `_time:<window>` for time filtering, e.g. `_time:10m`, `_time:1h`."
        ),
    )
    limit: int = Field(
        default=50,
        ge=1,
        le=1000,
        description="Maximum number of log entries to return (default 50).",
    )


class ErrorCountQuery(BaseModel):
    time_window: str = Field(
        default="1h",
        description="Time window for counting errors, e.g. '10m', '1h', '24h'.",
    )
    service: str = Field(
        default="",
        description="Optional service name filter. Leave empty for all services.",
    )


class TraceListQuery(BaseModel):
    service: str = Field(
        default="",
        description="Optional service name to filter traces. Leave empty for all services.",
    )
    limit: int = Field(
        default=20,
        ge=1,
        le=100,
        description="Maximum number of traces to return (default 20).",
    )


class TraceGetQuery(BaseModel):
    trace_id: str = Field(description="The trace ID to fetch.")


ToolPayload = BaseModel | Sequence[BaseModel] | dict | list | str
ToolHandler = Callable[
    [VictoriaLogsClient, VictoriaTracesClient, BaseModel], Awaitable[ToolPayload]
]


@dataclass(frozen=True, slots=True)
class ToolSpec:
    name: str
    description: str
    model: type[BaseModel]
    handler: ToolHandler

    def as_tool(self) -> Tool:
        schema = self.model.model_json_schema()
        schema.pop("$defs", None)
        schema.pop("title", None)
        return Tool(name=self.name, description=self.description, inputSchema=schema)


async def _logs_search(
    logs_client: VictoriaLogsClient,
    _traces_client: VictoriaTracesClient,
    args: BaseModel,
) -> ToolPayload:
    """Search logs using a LogsQL query."""
    query = args.query  # type: ignore[attr-defined]
    limit = args.limit  # type: ignore[attr-defined]

    results = await logs_client.query_logs(query, limit=limit)

    if not results:
        return "No log entries found for the given query."

    # Format results as concise summaries
    formatted = []
    for entry in results:
        parts = []
        timestamp = entry.pop("_time", entry.pop("@timestamp", ""))
        if timestamp:
            parts.append(f"[{timestamp}]")

        severity = entry.pop("severity", entry.pop("level", ""))
        if severity:
            parts.append(f"[{severity}]")

        service = entry.pop("service.name", entry.pop("service", ""))
        if service:
            parts.append(f"[{service}]")

        event = entry.pop("event", "")
        if event:
            parts.append(f"event={event}")

        # Include key fields like trace_id, error, status
        trace_id = entry.pop("trace_id", entry.pop("traceID", ""))
        if trace_id:
            parts.append(f"trace_id={trace_id}")

        error = entry.pop("error", entry.pop("message", ""))
        if error and severity.upper() in ("ERROR", "FATAL", "CRITICAL"):
            parts.append(f"error={error}")

        status = entry.pop("http.status_code", entry.pop("status_code", entry.pop("status", "")))
        if status:
            parts.append(f"status={status}")

        # Add remaining fields as key=value
        for key, value in sorted(entry.items()):
            if key not in ("_msg", "msg", "body"):
                parts.append(f"{key}={value}")

        # Include message/body if present
        msg = entry.get("_msg", entry.get("msg", entry.get("body", "")))
        if msg:
            parts.append(f'"{msg}"')

        formatted.append(" ".join(parts))

    return "\n".join(formatted)


async def _logs_error_count(
    logs_client: VictoriaLogsClient,
    _traces_client: VictoriaTracesClient,
    args: BaseModel,
) -> ToolPayload:
    """Count errors per service over a time window."""
    time_window = args.time_window  # type: ignore[attr-defined]
    service = args.service  # type: ignore[attr-defined]

    results = await logs_client.count_errors(
        time_window=time_window,
        service=service if service else None,
    )

    if not results:
        return f"No errors found in the last {time_window}."

    lines = [f"Error count (last {time_window}):"]
    for entry in sorted(results, key=lambda x: x["error_count"], reverse=True):
        lines.append(f"  {entry['service']}: {entry['error_count']} errors")

    return "\n".join(lines)


async def _traces_list(
    _logs_client: VictoriaLogsClient,
    traces_client: VictoriaTracesClient,
    args: BaseModel,
) -> ToolPayload:
    """List recent traces."""
    service = args.service  # type: ignore[attr-defined]
    limit = args.limit  # type: ignore[attr-defined]

    results = await traces_client.list_traces(
        service=service if service else None,
        limit=limit,
    )

    if not results:
        return "No traces found."

    lines = [f"Recent traces ({len(results)} found):"]
    for trace in results[:limit]:
        trace_id = trace.get("traceID", trace.get("trace_id", "unknown"))
        spans = trace.get("spans", [])
        svc = trace.get("processes", {})
        # Get service name from first span's process
        first_span = spans[0] if spans else {}
        process_id = first_span.get("processID", "")
        process = svc.get(process_id, {})
        service_name = ""
        for tag in process.get("tags", []):
            if tag.get("key") == "service.name":
                service_name = tag.get("value", "")
                break

        duration_ms = 0
        if spans:
            start = min(s.get("startTime", 0) for s in spans)
            end = max(s.get("startTime", 0) + s.get("duration", 0) for s in spans)
            duration_ms = end - start

        lines.append(
            f"  trace_id={trace_id} service={service_name or 'n/a'} "
            f"spans={len(spans)} duration={duration_ms}ms"
        )

    return "\n".join(lines)


async def _traces_get(
    _logs_client: VictoriaLogsClient,
    traces_client: VictoriaTracesClient,
    args: BaseModel,
) -> ToolPayload:
    """Fetch a specific trace by ID and show its span hierarchy."""
    trace_id = args.trace_id  # type: ignore[attr-defined]

    trace = await traces_client.get_trace(trace_id)
    if trace is None:
        return f"No trace found with ID: {trace_id}"

    spans = trace.get("spans", [])
    processes = trace.get("processes", {})

    lines = [f"Trace {trace_id} ({len(spans)} spans):"]

    # Build process ID -> service name map
    service_map: dict[str, str] = {}
    for proc_id, proc in processes.items():
        for tag in proc.get("tags", []):
            if tag.get("key") == "service.name":
                service_map[proc_id] = tag.get("value", proc_id)
                break

    # Show spans with hierarchy
    for span in sorted(spans, key=lambda s: s.get("startTime", 0)):
        span_id = span.get("spanID", "unknown")
        operation = span.get("operationName", "unknown")
        process_id = span.get("processID", "")
        service = service_map.get(process_id, process_id or "unknown")
        duration = span.get("duration", 0)
        depth = 0
        refs = span.get("references", [])
        if refs:
            depth = 1  # child span

        indent = "  " * depth
        tags = span.get("tags", [])
        error_tag = any(
            t.get("key") == "error" and t.get("value")
            for t in tags
        )
        error_suffix = " **ERROR**" if error_tag else ""

        # Check span-level status
        span_status = span.get("status", {})
        if span_status.get("status_code") == "STATUS_CODE_ERROR":
            error_suffix = " **ERROR**"

        lines.append(
            f"{indent}[{service}] {operation} ({duration}ms){error_suffix}"
        )

        # Show error details if present
        if error_tag or span_status.get("status_code") == "STATUS_CODE_ERROR":
            for tag in tags:
                if tag.get("key") in ("error", "error.message", "error.type"):
                    lines.append(f"{indent}    {tag['key']}={tag.get('value')}")

            # Check logs for error events
            logs = span.get("logs", [])
            for log_entry in logs:
                for field in log_entry.get("fields", []):
                    if field.get("key") in ("error", "event", "message"):
                        lines.append(f"{indent}    log: {field.get('key')}={field.get('value')}")

    return "\n".join(lines)


TOOL_SPECS = (
    ToolSpec(
        "logs_search",
        "Search structured logs in VictoriaLogs using a LogsQL query. "
        "Use `_time:<window>` for time filtering (e.g. `_time:10m`, `_time:1h`), "
        '`service.name:"ServiceName"` for service, `severity:ERROR` for errors.',
        LogSearchQuery,
        _logs_search,
    ),
    ToolSpec(
        "logs_error_count",
        "Count errors per service over a time window in VictoriaLogs. "
        "Returns a summary of error counts grouped by service name.",
        ErrorCountQuery,
        _logs_error_count,
    ),
    ToolSpec(
        "traces_list",
        "List recent traces from VictoriaTraces. "
        "Optionally filter by service name. Returns trace IDs, span counts, and durations.",
        TraceListQuery,
        _traces_list,
    ),
    ToolSpec(
        "traces_get",
        "Fetch a specific trace by ID from VictoriaTraces and show the span hierarchy. "
        "Use the trace_id from log entries or traces_list output.",
        TraceGetQuery,
        _traces_get,
    ),
)
TOOLS_BY_NAME = {spec.name: spec for spec in TOOL_SPECS}
