"""Shared pytest configuration for automated tests."""


def pytest_collection_modifyitems(items):
    """Apply suite markers based on the automated-tests subdirectory."""
    marker_by_dir = {
        "test_core": "core",
        "test_feedback": "feedback",
        "integration": "integration",
    }

    for item in items:
        path_parts = set(item.path.parts)
        for dirname, marker in marker_by_dir.items():
            if dirname in path_parts:
                item.add_marker(marker)
                break
