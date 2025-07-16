import datetime
import json
from pathlib import Path
import sqlite3

# from .dataset import Dataset, initialize_dataset, clear_dataset, contains_dataset
from .. import __version__


# def normalize_kind(kind: str) -> str:
#     # TODO
#     return kind
#
#
# def database_path(prefix: Path) -> Path:
#     assert prefix.is_dir()
#
#     return prefix.joinpath("trekr.json")


def adapt_time_point_iso(time_point: datetime.datetime) -> str:
    """Adapt datetime.datetime to timezone-naive ISO 8601 date."""
    return time_point.isoformat(timespec="minutes")


def convert_time_point(time_point: bytes) -> datetime.datetime:
    """Convert ISO 8601 datetime to datetime.datetime object."""
    return datetime.datetime.fromisoformat(time_point.decode("utf-8"))


sqlite3.register_adapter(datetime.datetime, adapt_time_point_iso)
sqlite3.register_converter("datetime", convert_time_point)


def table_exists(cursor: sqlite3.Cursor, name: str) -> bool:
    results = cursor.execute(f"""
        SELECT name FROM sqlite_master WHERE type='table' AND name='{name}'
    """)
    return len(results.fetchall()) == 1


class Database(object):
    # Class for representing the current version of the database. Old versions first need to be upgraded.

    def __init__(self, path: Path):
        self.path = path

        with sqlite3.connect(path) as connection:
            cursor = connection.cursor()

            assert table_exists(cursor, name="trekr")
            # assert table_exists(cursor, name="property_kind")
            # assert table_exists(cursor, name="property")
            # assert table_exists(cursor, name="magnitude")

            results = cursor.execute("""
                SELECT property, value from trekr WHERE property='version'
            """)
            properties = results.fetchall()
            assert len(properties) == 1, properties
            version = int(properties[0][1])

        assert version == __version__, f"{version} != {__version__}"

        self._version = version

    @property
    def version(self):
        return self._version

    # def dataset_idx(self, kind: str) -> int:
    #     result = -1
    #
    #     for idx, dataset in enumerate(self.datasets):
    #         if dataset.kind == kind:
    #             result = idx
    #             break
    #
    #     assert result >= 0
    #
    #     return result
    #
    # def dataset_exists(self, kind: str) -> bool:
    #     datasets = [dataset for dataset in self.datasets if dataset.kind == kind]
    #     assert 0 <= len(datasets) <= 1
    #
    #     return len(datasets) == 1
    #
    # def add_dataset(self, kind: str, *, unit: str) -> Dataset:
    #     if self.dataset_exists(kind):
    #         raise RuntimeError(
    #             f"Cannot add dataset: a dataset for kind {kind} already exists"
    #         )
    #
    #     dataset_directory_name = f"{normalize_kind(kind)}"
    #     dataset_path = self.path.joinpath(dataset_directory_name)
    #
    #     # Create the associated files
    #     dataset_path.mkdir()
    #     initialize_dataset(dataset_path, kind, unit)
    #
    #     # Reference the dataset
    #     self.datasets.append(Dataset(dataset_path))
    #
    #     return self.datasets[-1]
    #
    # def remove_dataset(self, kind: str) -> None:
    #     if not self.dataset_exists(kind):
    #         raise RuntimeError(
    #             f"Cannot remove dataset: a dataset for kind {kind} does not exist"
    #         )
    #
    #     dataset_directory_name = f"{normalize_kind(kind)}"
    #     dataset_path = self.path.joinpath(dataset_directory_name)
    #
    #     # Dereference the dataset
    #     del self.datasets[self.dataset_idx(kind)]
    #
    #     # Remove the associated files
    #     clear_dataset(dataset_path)
    #     dataset_path.rmdir()


def initialize_database(path: Path) -> None:
    if path.exists():
        if path.is_file():
            raise RuntimeError(
                f"Cannot initialize database: a file with name {path} already exists"
            )
        elif path.is_dir():
            raise RuntimeError(
                f"Cannot initialize database: a directory with name {path} already exists"
            )
    else:
        parent_path = path.parent

        if not parent_path.is_dir():
            raise RuntimeError(
                f"Cannot initialize database: parent directory {parent_path} does not exist"
            )

    assert not path.exists(), path

    with sqlite3.connect(path) as connection:
        cursor = connection.cursor()

        cursor.execute("""
            PRAGMA foreign_keys = ON
        """)

        # trekr: | property | value |
        cursor.execute("""
            CREATE TABLE trekr(
                property TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
        """)
        cursor.execute("INSERT INTO trekr (property, value) VALUES ('version', '0')")

        # Built-in table with information about quantities
        # trekr_quantity: | name | description |
        cursor.execute("""
            CREATE TABLE trekr_quantity(
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT NOT NULL
            )
        """)
        data = (
            {
                "id": 0,
                "name": "mass",
                "description": "TODO",
            },
            {
                "id": 1,
                "name": "distance",
                "description": "TODO",
            },
            {
                "id": 2,
                "name": "time",
                "description": "TODO",
            },
        )
        cursor.executemany(
            "INSERT INTO trekr_quantity VALUES(:id, :name, :description)", data
        )

        # Built-in table with information about units
        # trekr_unit: | name | description |
        cursor.execute("""
            CREATE TABLE trekr_unit(
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT NOT NULL
            )
        """)
        data = (
            {
                "id": 0,
                "name": "kilogram",
                "description": "TODO",
            },
            {
                "id": 1,
                "name": "meter",
                "description": "TODO",
            },
            {
                "id": 2,
                "name": "hour",
                "description": "TODO",
            },
        )
        cursor.executemany(
            "INSERT INTO trekr_unit VALUES(:id, :name, :description)", data
        )

        # Built-in table with per quantity one or more units
        # trekr_quantity_unit: | trekr_quantity_id | trekr_unit_id |
        cursor.execute("""
            CREATE TABLE trekr_quantity_unit(
                quantity_id INTEGER,
                unit_id INTEGER,
                PRIMARY KEY (quantity_id, unit_id),
                FOREIGN KEY (quantity_id) REFERENCES trekr_quantity (id),
                FOREIGN KEY (unit_id) REFERENCES trekr_unit (id)
            )
        """)
        data = (
            {
                "quantity_id": 0,
                "unit_id": 0,
            },
            {
                "quantity_id": 1,
                "unit_id": 1,
            },
            {
                "quantity_id": 2,
                "unit_id": 2,
            },
        )
        cursor.executemany(
            "INSERT INTO trekr_quantity_unit VALUES(:quantity_id, :unit_id)", data
        )

        # User table for storing information about trekked quantities
        # quantity: | quantity_id | unit_id | name | description | context |
        cursor.execute("""
            CREATE TABLE quantity(
                quantity_id INTEGER,
                unit_id INTEGER,
                name TEXT NOT NULL,
                description TEXT,
                context TEXT,
                PRIMARY KEY (quantity_id, unit_id, name),
                FOREIGN KEY (quantity_id) REFERENCES trekr_quantity (id),
                FOREIGN KEY (unit_id) REFERENCES trekr_unit (id)
            )
        """)

        # User table for storing information about trekked contexts
        # context: | context_id | name |
        cursor.execute("""
            CREATE TABLE context(
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL
            )
        """)

        # value: | quantity_id | context_id | date | value |
        cursor.execute("""
            CREATE TABLE value(
                quantity_id INTEGER,
                context_id INTEGER,
                date datetime NOT NULL,
                value REAL NOT NULL,
                FOREIGN KEY (context_id) REFERENCES context (id)
            )
        """)


def upgrade_database_0_1(path: Path) -> None:
    with sqlite3.connect(path) as connection:
        cursor = connection.cursor()
        cursor.execute("UPDATE trekr SET value='1' WHERE property='version'")


def upgrade_database(path: Path) -> None:
    with sqlite3.connect(path) as connection:
        cursor = connection.cursor()

        results = cursor.execute("""
            SELECT property, value from trekr WHERE property='version'
        """)
        properties = results.fetchall()
        assert len(properties) == 1, properties
        database_version = int(properties[0][1])

    current_version = __version__

    # If database version is smaller than current version, make any necessary changes
    if database_version < current_version:
        if database_version == 0:
            upgrade_database_0_1(path)


def add_database(path: Path) -> Database:
    # - Initialize database, version 0
    # - Upgrade database to current version

    initialize_database(path)
    upgrade_database(path)

    return Database(path)


def database_exists(path: Path) -> bool:
    return path.is_file()


def remove_database(path: Path) -> None:
    if not database_exists(path):
        raise RuntimeError(
            f"Cannot remove database {path}: it doesn't seem to be a valid database"
        )

    path.unlink()
