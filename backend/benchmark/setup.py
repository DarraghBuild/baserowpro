#!/usr/bin/env python3

import argparse
import subprocess
from pathlib import Path

import psycopg2
from django.conf import settings

DEFAULT_DB = settings.DATABASES["default"]

parser = argparse.ArgumentParser()
parser.add_argument(
    "--initdb",
    action="store_true",
    help="Should the current database be replaced with our benchmarking database?",
)


class BenchmarkSetup:
    @classmethod
    def initdb(cls):
        connection = psycopg2.connect(
            database="postgres",
            user=DEFAULT_DB["USER"],
            password=DEFAULT_DB["PASSWORD"],
            host=DEFAULT_DB["HOST"],
        )
        connection.autocommit = True
        cursor = connection.cursor()
        confirm = input(
            "Calling --initdb will drop your current database, are you "
            "sure you want to do this? y/n\n"
        ).lower()
        if confirm != "y":
            return

        # Double-check the grid view many field SQL exists.
        if not Path("samples/grid-view-many-fields.sql").is_file():
            raise EnvironmentError("Please download the sample SQL.")

        try:
            cursor.execute(f"DROP DATABASE IF EXISTS {DEFAULT_DB['NAME']}")
            cursor.execute(f"CREATE DATABASE {DEFAULT_DB['NAME']}")
        except psycopg2.errors.ObjectInUse:
            raise EnvironmentError("The database cannot be re-created if it is use.")

        subprocess.run(
            f"psql -U {DEFAULT_DB['USER']} -h {DEFAULT_DB['HOST']} "
            f"{DEFAULT_DB['NAME'] } < samples/grid-view-many-fields.sql",
            shell=True,
            env={"PGPASSWORD": DEFAULT_DB["PASSWORD"]},
        )


if __name__ == "__main__":
    args = parser.parse_args()
    if args.initdb:
        BenchmarkSetup.initdb()
