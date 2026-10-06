"""Custom state reducers for the reporting agent graph.

Each reducer merges a node's partial update into the shared state without
clobbering existing values; they are attached to state fields via ``Annotated``.
"""


def add_policies(existing: list[dict], new: list[dict]) -> list[dict]:
    """Merge policy entries, de-duplicating by policy id.

    Args:
        existing (list[dict]): Policies already in state.
        new (list[dict]): Policies returned by a node.

    Returns:
        list[dict]: The union keyed by ``id`` (later entries win).
    """
    by_id = {p["id"]: p for p in existing or []}
    for p in new or []:
        by_id[p["id"]] = p
    return list(by_id.values())


def add_people(existing: list[dict], new: list[dict]) -> list[dict]:
    """Merge people, de-duplicating by ``(name, role)``.

    Args:
        existing (list[dict]): People already in state.
        new (list[dict]): People returned by a node.

    Returns:
        list[dict]: The union keyed by ``(name, role)``.
    """
    by_key = {(p["name"], p["role"]): p for p in existing or []}
    for p in new or []:
        by_key[(p["name"], p["role"])] = p
    return list(by_key.values())


def merge_info(existing: dict, new: dict) -> dict:
    """Shallow-merge report header scalars, the latest value winning.

    Args:
        existing (dict): Header scalars already in state.
        new (dict): Header scalars returned by a node.

    Returns:
        dict: The merged mapping.
    """
    return {**(existing or {}), **(new or {})}


def take_latest(existing: object, new: object) -> object:
    """Overwrite with the newest value, keeping the old one when none is given.

    Used for the scalar ``phase`` field: whichever node most recently set a phase
    wins, and nodes that omit it leave the current phase untouched.

    Args:
        existing (object): Value already in state.
        new (object): Value returned by a node (``None`` to keep ``existing``).

    Returns:
        object: ``new`` when it is not ``None``, otherwise ``existing``.
    """
    return new if new is not None else existing
