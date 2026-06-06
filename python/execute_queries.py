from pathlib import Path

import pandas as pd

try:
    from .db_connection import get_mysql_engine
    from .helper_functions import PROJECT_ROOT, ensure_output_dirs
except ImportError:
    from db_connection import get_mysql_engine
    from helper_functions import PROJECT_ROOT, ensure_output_dirs


QUERY_DIR = PROJECT_ROOT / "database"
OUTPUT_DIR = PROJECT_ROOT / "outputs" / "query_results"


def run_query(sql):
    engine = get_mysql_engine()
    return pd.read_sql(sql, engine)


def save_named_query(name, sql):
    ensure_output_dirs()
    result = run_query(sql)
    output_path = OUTPUT_DIR / f"{name}.csv"
    result.to_csv(output_path, index=False)
    return output_path


if __name__ == "__main__":
    sql = "SELECT booking_status, COUNT(*) AS bookings FROM ola_bookings GROUP BY booking_status;"
    path = save_named_query("booking_status_distribution", sql)
    print(f"Saved query result to {path}")
