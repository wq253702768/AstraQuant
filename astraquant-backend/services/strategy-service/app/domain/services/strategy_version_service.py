from decimal import Decimal


def next_version(existing_versions: list[str]) -> str:
    if not existing_versions:
        return "v1.0"
    max_major = 1
    max_minor = -1
    for version in existing_versions:
        normalized = version.removeprefix("v")
        try:
            major_raw, minor_raw = normalized.split(".", 1)
            major, minor = int(major_raw), int(minor_raw)
        except ValueError:
            continue
        if (major, minor) > (max_major, max_minor):
            max_major, max_minor = major, minor
    if max_minor < 0:
        return "v1.0"
    return f"v{max_major}.{max_minor + 1}"
