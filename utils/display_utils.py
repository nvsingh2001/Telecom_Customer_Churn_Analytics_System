import os
import subprocess


def clear():
    subprocess.call("cls" if os.name == "nt" else "clear")


def print_table(headers, rows):
    if not rows:
        print("[No data found]")
        return

    # Determine column widths
    widths = [len(h) for h in headers]
    for row in rows:
        for i, val in enumerate(row):
            widths[i] = max(widths[i], len(str(val)))

    # Print header
    header_row = " | ".join(f"{headers[i]:<{widths[i]}}" for i in range(len(headers)))
    print("\n" + header_row)
    print("-" * len(header_row))

    # Print rows
    for row in rows:
        print(" | ".join(f"{str(row[i]):<{widths[i]}}" for i in range(len(row))))


def format_redshift_records(result):
    """
    Flattens Redshift Data API results into a list of lists.
    """
    formatted = []
    if not result or "Records" not in result:
        return formatted

    for record in result["Records"]:
        row = []
        for col in record:
            # The Data API returns values as a dictionary with the type as the key
            # e.g., {'stringValue': 'London'} or {'longValue': 123}
            if col:
                value = list(col.values())[0]
            else:
                value = None
            row.append(value)
        formatted.append(row)
    return formatted
