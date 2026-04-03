"""HTTP client for VictoriaLogs and VictoriaTraces APIs."""

from __future__ import annotations

from typing import Any
from urllib.parse import urlencode

import httpx


class VictoriaLogsClient:
    """Client for the VictoriaLogs HTTP API."""

    def __init__(
        self,
        base_url: str,
        *,
        http_client: httpx.AsyncClient | None = None,
        timeout: float = 15.0,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self._owns_client = http_client is None
        self._http_client = http_client or httpx.AsyncClient(
            base_url=self.base_url,
            timeout=timeout,
        )

    async def __aenter__(self) -> "VictoriaLogsClient":
        return self

    async def __aexit__(self, *_: object) -> None:
        await self.aclose()

    async def aclose(self) -> None:
        if self._owns_client:
            await self._http_client.aclose()

    async def query_logs(
        self,
        query: str,
        *,
        limit: int = 100,
        start: str | None = None,
        end: str | None = None,
    ) -> list[dict[str, Any]]:
        """Search logs using LogsQL query.

        VictoriaLogs /select/logsql/query endpoint returns newline-delimited JSON
        (one JSON object per line).
        """
        params: dict[str, str | int] = {"query": query, "limit": limit}
        if start:
            params["start"] = start
        if end:
            params["end"] = end

        response = await self._http_client.post(
            "/select/logsql/query",
            content=urlencode(params).encode(),
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        response.raise_for_status()

        results: list[dict[str, Any]] = []
        for line in response.text.strip().splitlines():
            line = line.strip()
            if line:
                try:
                    results.append(httpx._compat.decode(line))
                except Exception:
                    import json

                    try:
                        results.append(json.loads(line))
                    except Exception:
                        pass
        return results

    async def count_errors(
        self,
        *,
        service: str | None = None,
        time_window: str = "1h",
    ) -> list[dict[str, Any]]:
        """Count errors per service over a time window.

        Uses the stats endpoint for aggregation.
        """
        query = f"_time:{time_window} severity:ERROR"
        if service:
            query += f' service.name:"{service}"'

        # Use regular query — parse results and count
        results = await self.query_logs(query, limit=10000)

        # Group by service.name
        counts: dict[str, int] = {}
        for entry in results:
            svc = entry.get("service.name", entry.get("service", "unknown"))
            counts[svc] = counts.get(svc, 0) + 1

        return [{"service": svc, "error_count": cnt} for svc, cnt in counts.items()]


class VictoriaTracesClient:
    """Client for the VictoriaTraces Jaeger-compatible HTTP API."""

    def __init__(
        self,
        base_url: str,
        *,
        http_client: httpx.AsyncClient | None = None,
        timeout: float = 15.0,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self._owns_client = http_client is None
        self._http_client = http_client or httpx.AsyncClient(
            base_url=self.base_url,
            timeout=timeout,
        )

    async def __aenter__(self) -> "VictoriaTracesClient":
        return self

    async def __aexit__(self, *_: object) -> None:
        await self.aclose()

    async def aclose(self) -> None:
        if self._owns_client:
            await self._http_client.aclose()

    async def list_traces(
        self,
        *,
        service: str | None = None,
        limit: int = 20,
    ) -> list[dict[str, Any]]:
        """List recent traces.

        Uses the Jaeger-compatible /select/jaeger/api/traces endpoint.
        """
        params: dict[str, str | int] = {"limit": limit}
        if service:
            params["service"] = service

        response = await self._http_client.get(
            "/select/jaeger/api/traces", params=params
        )
        response.raise_for_status()
        data = response.json()
        return data.get("data", [])

    async def get_trace(self, trace_id: str) -> dict[str, Any] | None:
        """Fetch a specific trace by ID.

        Uses the Jaeger-compatible /select/jaeger/api/traces/<traceID> endpoint.
        """
        response = await self._http_client.get(
            f"/select/jaeger/api/traces/{trace_id}"
        )
        response.raise_for_status()
        data = response.json()
        traces = data.get("data", [])
        if traces:
            return traces[0]
        return None
