import datetime
import json
from pathlib import Path, PurePosixPath
import sqlite3
import networkx as nx

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


def context_from_string(context: nx.DiGraph) -> str:
    context_as_dict = nx.to_dict_of_dicts(context)

    return json.dumps(context_as_dict)


def context_to_string(context_as_string: str) -> nx.DiGraph:
    context_as_dict = json.loads(context_as_string)

    return nx.from_dict_of_dicts(context_as_dict)


class Database(object):
    # Class for representing the current version of the database. Old versions first need to be upgraded.

    def __init__(self, path: Path):
        self.path = path

        with sqlite3.connect(path) as connection:
            cursor = connection.cursor()

            assert table_exists(cursor, name="trekr")
            assert table_exists(cursor, name="trekr_quantity")
            assert table_exists(cursor, name="trekr_unit")
            assert table_exists(cursor, name="trekr_quantity_unit")
            assert table_exists(cursor, name="quantity")
            assert table_exists(cursor, name="segment")
            assert table_exists(cursor, name="value")

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

    def trekr_quantity_id(self, cursor: sqlite3.Cursor, name: str) -> int:
        results = cursor.execute(f"""
            SELECT id FROM trekr_quantity WHERE name='{name}'
        """).fetchall()
        assert len(results) == 1, results
        return results[0][0]

    def trekr_unit_id(self, cursor: sqlite3.Cursor, name: str) -> int:
        results = cursor.execute(f"""
            SELECT id FROM trekr_unit WHERE name='{name}'
        """).fetchall()
        assert len(results) == 1, results
        return results[0][0]

    def quantity_id(
        self, cursor: sqlite3.Cursor, quantity_id: int, unit_id: int, name: str
    ) -> int:
        results = cursor.execute(f"""
            SELECT id FROM quantity WHERE quantity_id={quantity_id} AND unit_id={unit_id} AND name='{name}'
        """).fetchall()
        assert len(results) == 1, results
        return results[0][0]

    def add_quantity(
        self,
        quantity: str,
        unit: str,
        name: str,
        description: str,
        context: nx.DiGraph,
    ) -> None:
        context_as_string = context_from_string(context)

        with sqlite3.connect(self.path) as connection:
            cursor = connection.cursor()
            quantity_id = self.trekr_quantity_id(cursor, quantity)
            unit_id = self.trekr_unit_id(cursor, unit)
            cursor.execute(f"""
                INSERT INTO quantity (quantity_id, unit_id, name, description, context)
                VALUES ({quantity_id}, {unit_id}, '{name}', '{description}', '{context_as_string}')
            """)
            quantity_id = self.quantity_id(cursor, quantity_id, unit_id, name)

        return quantity_id

    def add_value(
        self,
        quantity_id: int,
        context_path: PurePosixPath,
        date: datetime.datetime,
        value: float,
    ) -> None:
        # - Given the quantity_id, obtain the context tree. The context tree is a tree of unique IDs.
        # - The context_path passed in contains names, which can be translated to a path of unique IDs, using
        #   the context table. For any context segment in the context_path which cannot be found in the
        #   context table, a unique ID has to be determined which has to be added to the context tree and the
        #   context table.
        # - Given the quantity_id, and the ID of the last node of the context_path, add a record to the value
        #   table
        # TODO: Implement
        assert not context_path.is_absolute(), context_path

        # context_tree = self.context_tree(quantity_id)
        # context_segments = self.context_segments(quantity_id)
        # segment_names = context_path.parts

        # Annotate context_tree of node IDs with node names, given information from context_segments
        # Determine which part of context_path, if any, is not present in the context tree
        # Add missing segments to the tree node IDs and node names. Write updated tree to quantity table.
        # Write new segment IDs and names to segment table.
        # Add record for quantity_id, node segment ID, date and value to value table

        pass

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
                id INTEGER PRIMARY KEY,
                quantity_id INTEGER,
                unit_id INTEGER,
                name TEXT NOT NULL,
                description TEXT,
                context TEXT,
                UNIQUE (quantity_id, unit_id, name),
                FOREIGN KEY (quantity_id) REFERENCES trekr_quantity (id),
                FOREIGN KEY (unit_id) REFERENCES trekr_unit (id)
            )
        """)

        # User table for storing information about trekked contexts. A context tree is associated with a
        # quantity. Within the tree, nodes are represented by unique IDs. Between trees, node IDs don't
        # have to be unique.
        # segment: | quantity_id | segment_id | name |
        cursor.execute("""
            CREATE TABLE segment(
                quantity_id INTEGER NOT NULL,
                segment_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                PRIMARY KEY (quantity_id, segment_id),
                FOREIGN KEY (quantity_id) REFERENCES quantity (id)
            )
        """)

        # value: | quantity_id | segment_id | date | value |
        cursor.execute("""
            CREATE TABLE value(
                quantity_id INTEGER NOT NULL,
                segment_id INTEGER NOT NULL,
                date datetime NOT NULL,
                value REAL NOT NULL,
                PRIMARY KEY (quantity_id, segment_id),
                FOREIGN KEY (quantity_id) REFERENCES quentity (id),
                FOREIGN KEY (segment_id) REFERENCES context (id)
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
