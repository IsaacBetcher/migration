import csv

from config import (
    PROJECT_DB_ID,
    EMPLOYEE_DB_ID,
)
from parser import (
    load_csv_rows,
    load_indiv_csv,
    load_tues_csv,
)
from relation_lookup import fetch_relation_lookup
from updater import (
    build_properties,
    create_page,
)


# MAIN

def main():

    # "group" -> monday_checks - group.csv
    # "ind" -> monday_checks - ind.csv
    # "tues" -> monday_checks - tues.csv
    IMPORT_TYPE = "tues"  # should be called group, ind, or tues depending on the csv file exported

    print("Starting Monday Check Import...")

    print("Loading relation lookups...")

    project_lookup = fetch_relation_lookup(
        PROJECT_DB_ID,
        "Name"
    )

    employee_lookup = fetch_relation_lookup(
        EMPLOYEE_DB_ID,
        "Name"
    )

    print("Project lookup loaded.")
    print("Employee lookup loaded.")

    print(f"Import type selected: {IMPORT_TYPE}")

    if IMPORT_TYPE == "group":
        rows = load_csv_rows("csv_files/monday_checks - group.csv")

    elif IMPORT_TYPE == "ind":
        rows = load_indiv_csv("csv_files/monday_checks - ind.csv")
    elif IMPORT_TYPE == "tues":
        rows = load_tues_csv("csv_files/monday_checks - tues.csv")

    else:
        print(f"ERROR: Invalid IMPORT_TYPE -> {IMPORT_TYPE}")
        return

    print(f"Loaded {len(rows)} rows from CSV.")

    success = 0
    failed = 0
    skipped = 0
    error_log = []

    for i, row in enumerate(rows, start=1):
        try:
            print(f"\nProcessing Row {i}...")

            unique_key, properties = build_properties(
                row,
                project_lookup,
                employee_lookup
            )

            if not properties:
                skipped += 1
                print(f"[{i}] SKIPPED -> No valid properties built")
                continue

            create_page(properties)

            success += 1
            print(
                f"[{i}] SUCCESS -> Created: "
                f"{row.get('Monday Check Name', 'Unknown')}"
            )

        except Exception as e:
            failed += 1

            print(f"[{i}] FAILED -> {str(e)}")

            error_log.append({
                "row_number": i,
                "title": row.get("Monday Check Name", ""),
                "error": str(e)
            })

    if error_log:
        with open(
            "logs/errors.csv",
            "w",
            newline="",
            encoding="utf-8"
        ) as file:
            writer = csv.DictWriter(
                file,
                fieldnames=["row_number", "title", "error"]
            )

            writer.writeheader()
            writer.writerows(error_log)

        print("\nError log written to logs/errors.csv")

    print("\n=====================================")
    print("IMPORT COMPLETE")
    print("=====================================")
    print(f"Successful Imports: {success}")
    print(f"Skipped Rows:       {skipped}")
    print(f"Failed Rows:        {failed}")
    print("=====================================")


if __name__ == "__main__":
    main()

# MAIN EXTRA

def process_row(row, project_lookup, employee_lookup):
    try:
        unique_key, properties = build_properties(
            row,
            project_lookup,
            employee_lookup
        )

        if not properties:
            return "SKIPPED", "No properties built"

        create_page(properties)

        return "SUCCESS", unique_key

    except Exception as e:
        return "FAILED", str(e)
