import datetime
from pathlib import Path, PurePosixPath
import tempfile
import unittest

import networkx as nx

from trekr import __version__
from trekr import io


class DatabaseTest(unittest.TestCase):
    def validate_newly_added_database(self, database):
        self.assertEqual(database.version, __version__)

    def test_add_database_non_existing_directory(self):
        with self.assertRaisesRegex(RuntimeError, "parent directory"):
            with tempfile.TemporaryDirectory() as directory_pathname:
                database_path = Path(directory_pathname).joinpath(
                    "doesnotexist", "my_database.sqlite3"
                )
                assert not database_path.parent.exists(), database_path.parent
                io.add_database(database_path)

    def test_add_database_existing_empty_directory(self):
        with tempfile.TemporaryDirectory() as directory_pathname:
            database_path = Path(directory_pathname).joinpath("my_database.sqlite3")
            database = io.add_database(database_path)
            self.validate_newly_added_database(database)

    def test_add_database_existing_file(self):
        with self.assertRaisesRegex(RuntimeError, "a file with name"):
            with tempfile.NamedTemporaryFile(delete_on_close=False) as fp:
                fp.close()
                database_path = Path(fp.name)
                io.add_database(database_path)

    def test_remove_database(self):
        with tempfile.TemporaryDirectory() as directory_pathname:
            path = Path(directory_pathname).joinpath("my_database.sqlite3")
            io.add_database(path)
            self.assertTrue(io.database_exists(path))
            io.remove_database(path)
            self.assertFalse(io.database_exists(path))
            self.assertFalse(path.exists())

    def test_define_quantity(self):
        with tempfile.TemporaryDirectory() as directory_pathname:
            path = Path(directory_pathname).joinpath("my_database.sqlite3")
            database = io.add_database(path)

            # Timesheet
            quantity_id = database.add_quantity(
                quantity="time",
                unit="hour",
                name="timesheet",
                description="My timesheet",
                context=nx.DiGraph(),
            )
            database.add_value(
                quantity_id=quantity_id,
                context_path=PurePosixPath("a/b/c"),
                date=datetime.datetime.now(),
                value=5.5,
            )

    # Test adding some information:
    # - Foreign key constraint (kind that doesn't exist for example)

    # context
    # - client/project(/sub_project)
    # - person/body(/weight)
    # - bike(/brand)
    # - shoe(/brand)

    # property
    # - sub_project (time/hours)
    # - weight (mass/kg)
    # - brand (distance/km)

    # quantity
    # - mass, time, distance, heat, angle

    # unit of measurement
    # - kg, seconds, meter, degrees Celsius, degrees

    # With the context, sub-contexts can be created/used, but these must all have the same quantity
    # - Context is the toplevel organizing structure, below which a sub-context hierarchy of properties can be
    #   stored
    #   - context:
    #     - client/project/time → (time/hours)
    #     - client/project/invoice → (money/euros)
    #   - property:
    #     - sub_project1/sub_project2

    # QUANTITY
    # - What do you want to trek (quantity)?
    #   → quantity: time
    # - What unit of measurement do you want to use for "time"?
    #   → unit: hours (pint package)
    # - How do you want to refer to this time quantity (what is its name)?
    #   → name: timesheet
    # - How would you describe timesheet (can be changed later)?
    #   → description: Number of hours worked on (sub-)projects

    # Adding records involves:
    # - Pick a quantity to add to
    # - Pick a context
    #   - A context is a path, e.g.: <client>/<sub_project1>/<sub_project2>
    #   - A context must have a unique ID. Use this ID as the node in the networkx tree.
    #   - A context can be partial. Its path does not have to contain a leaf node.
    #   - It must be possible to select one of the existing ones (from a tree visualization?)
    #   - It must be possible to add these on the fly, by typing a path (or by adding branches to the tree
    #     vis?)
    #   - It must be possible to rename contexts (by editing the tree vis?)
    # - Pick a date
    # - Enter a value (floating point)

    # Each context is part of a tree (arborescence in networkx-speak)
    # Each tree is associated with a quantity
    # Contexts together form a forest (branching in networkx-speak). This may not be useful. Keep each context
    # tree as its own thing, linked to a quantity. Each context tree stores values for the same quantity. Each
    # value is associated with a path into this tree.

    # context: time
    # property: <client>/<project>

    # https://en.wikipedia.org/wiki/Quantity
    # Add:
    # - quantity:
    #     - amount of something
    #     - property that can exist as a multitude or magnitude
    #     - example of quantitive properties:
    #       - mass, time, distance, heat, angle
    # - unit of measurement
    #     - magnitude of a quantity

    # def test_add_dataset(self):
    #     with tempfile.TemporaryDirectory() as directory_pathname:
    #         prefix = Path(directory_pathname)
    #         database = io.add_database(prefix)
    #         kind = "bike ride"
    #         unit = "km"
    #         self.assertFalse(database.dataset_exists(kind))
    #         dataset = database.add_dataset(kind, unit=unit)
    #         self.assertTrue(database.dataset_exists(kind))
    #         self.assertEqual(dataset.kind, kind)
    #         self.assertEqual(dataset.unit, unit)
    #
    # def test_remove_existing_dataset(self):
    #     with tempfile.TemporaryDirectory() as directory_pathname:
    #         prefix = Path(directory_pathname)
    #         database = io.add_database(prefix)
    #         kind = "bike ride"
    #         unit = "km"
    #         database.add_dataset(kind, unit=unit)
    #         self.assertTrue(database.dataset_exists(kind))
    #         database.remove_dataset(kind)
    #         self.assertFalse(database.dataset_exists(kind))
    #
    # def test_remove_non_existing_dataset(self):
    #     with tempfile.TemporaryDirectory() as directory_pathname:
    #         prefix = Path(directory_pathname)
    #         database = io.add_database(prefix)
    #         kind = "bike ride"
    #         with self.assertRaisesRegex(RuntimeError, "a dataset for kind"):
    #             database.remove_dataset(kind)
