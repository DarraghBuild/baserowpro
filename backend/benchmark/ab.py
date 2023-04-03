#!/usr/bin/env python3

import subprocess
import requests
from django.conf import settings


def get_token(username: str, password: str) -> str:
    response = requests.post(
        f"{settings.PUBLIC_BACKEND_URL}/api/user/token-auth/",
        {"username": username, "password": password},
    )
    response.raise_for_status()
    return response.json()["access_token"]


def generate_filename(operation_name: str, limit: int, concurrency: int) -> str:
    return f"{operation_name}_spike"


def ab(
    access_token: str,
    operation_name: str,
    endpoint: str,
    limit: int = 10,
    concurrency: int = 5,
):
    command = (
        f"ab -n {limit} -c {concurrency} -H 'Authorization: JWT {access_token}' "
        f"'{settings.PUBLIC_BACKEND_URL}{endpoint}'"
    )
    result = subprocess.run(command, shell=True, capture_output=True)
    filename = generate_filename(operation_name, limit, concurrency)
    with open(f"results/{filename}.txt", "w") as fs:
        fs.write(result.stdout.decode("utf8"))


if __name__ == "__main__":
    token = get_token("dev@baserow.io", "testpassword")
    cases = [
        {
            "operation": "list_database_table_rows",
            "url": "/api/database/views/grid/1910/?limit=80&offset=0",
        },
        {
            "operation": "search_database_rows",
            "url": "/api/database/views/grid/1910/"
            "?limit=120&offset=0&include=row_metadata&search=sarah",
        },
        {
            "operation": "aggregate_database_rows",
            "url": "/api/database/views/grid/1910/aggregations",
        },
    ]
    for case in cases:
        print(f"Benchmarking operation {case['operation']}")
        ab(token, case["operation"], case["url"], 10, 5)
