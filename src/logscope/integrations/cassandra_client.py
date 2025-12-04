from datetime import datetime
from typing import Dict, Iterable, List, Optional


class CassandraUnavailable(RuntimeError):
    pass


class CassandraIssueStore:
    """Persist issues to a Cassandra cluster.

    This class is deliberately minimal; it expects that the keyspace and table
    already exist. The table is assumed to have at least the following columns:

    - config_name (text)
    - recorded_at (timestamp)
    - issue (text/json)
    """

    def __init__(self, hosts: Iterable[str], keyspace: str, table: str):
        try:
            from cassandra.cluster import Cluster
        except ImportError as exc:  # pragma: no cover - exercised via tests
            raise CassandraUnavailable(
                "cassandra-driver is required to use CassandraIssueStore"
            ) from exc

        self._table = table
        self._session = Cluster(list(hosts)).connect(keyspace)

    def store(self, config_name: str, issues: List[dict]) -> None:
        payload = {
            "config_name": config_name,
            "recorded_at": datetime.utcnow(),
            "issues": issues,
        }
        self._session.execute(
            f"INSERT INTO {self._table} (config_name, recorded_at, issue) VALUES (%s, %s, %s)",
            (payload["config_name"], payload["recorded_at"], payload["issues"]),
        )

    def fetch(self, config_name: Optional[str] = None, limit: int = 100) -> Dict[str, List[List[dict]]]:
        query = f"SELECT config_name, recorded_at, issue FROM {self._table}"
        params: tuple = ()
        if config_name:
            query += " WHERE config_name = %s"
            params = (config_name,)
        query += " LIMIT %s"
        params = params + (limit,)
        rows = self._session.execute(query, params)
        result: Dict[str, List[List[dict]]] = {}
        for row in rows:
            result.setdefault(row.config_name, []).append(row.issue)
        return result


class InMemoryIssueStore:
    """Lightweight issue store for testing and offline usage."""

    def __init__(self):
        self._storage: Dict[str, List[List[dict]]] = {}

    def store(self, config_name: str, issues: List[dict]) -> None:
        self._storage.setdefault(config_name, []).append(issues)

    def fetch(self, config_name: Optional[str] = None) -> Dict[str, List[List[dict]]]:
        if config_name is None:
            return dict(self._storage)
        return {config_name: list(self._storage.get(config_name, []))}
