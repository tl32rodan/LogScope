from typing import Callable, Iterable, Iterator, Protocol

from logscope.model.issue import Issue


class IssueFilter(Protocol):
    def __call__(self, issue: Issue) -> bool:
        ...


def apply_filters(issues: Iterable[Issue], filters: Iterable[Callable[[Issue], bool]]) -> Iterator[Issue]:
    """Yield issues that pass all provided filter callables."""
    for issue in issues:
        if all(filter_fn(issue) for filter_fn in filters):
            yield issue


def exclude_by_owner(excluded_owner: str) -> IssueFilter:
    """Return a filter that removes issues belonging to a given owner."""
    def _filter(issue: Issue) -> bool:
        return issue.owner != excluded_owner

    return _filter
