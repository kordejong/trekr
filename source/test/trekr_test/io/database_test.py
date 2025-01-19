from pathlib import Path
import tempfile
import unittest

from trekr import __version__
from trekr import io


class DatabaseTest(unittest.TestCase):

    def validate_newly_added_database(self, database):
        self.assertEqual(database.version, __version__)
        self.assertEqual(len(database.datasets), 0)

    def test_add_database_non_existing_directory(self):
        with tempfile.TemporaryDirectory() as directory_pathname:
            prefix = Path(directory_pathname).joinpath("meh")
            database = io.add_database(prefix)
            self.validate_newly_added_database(database)

    def test_add_database_existing_empty_directory(self):
        with tempfile.TemporaryDirectory() as directory_pathname:
            prefix = Path(directory_pathname)
            database = io.add_database(prefix)
            self.validate_newly_added_database(database)

    def test_add_database_non_existing_parent_directory(self):
        with self.assertRaisesRegex(FileNotFoundError, "No such file or directory"):
            with tempfile.TemporaryDirectory() as directory_pathname:
                prefix = Path(directory_pathname).joinpath("meh", "mah")
                io.add_database(prefix)

    def test_add_database_existing_non_empty_directory(self):
        with self.assertRaisesRegex(RuntimeError, "exists and is not empty"):
            with tempfile.TemporaryDirectory() as directory_pathname:
                prefix = Path(directory_pathname)
                prefix.joinpath("mah").touch()
                io.add_database(prefix)

    def test_add_database_existing_file(self):
        with self.assertRaisesRegex(RuntimeError, "a regular file with name"):
            with tempfile.NamedTemporaryFile(delete_on_close=False) as fp:
                fp.close()
                prefix = Path(fp.name)
                io.add_database(prefix)

    def test_remove_database(self):
        with tempfile.TemporaryDirectory() as directory_pathname:
            prefix = Path(directory_pathname).joinpath("meh")
            io.add_database(prefix)
            self.assertTrue(io.database_exists(prefix))
            io.remove_database(prefix)
            self.assertFalse(io.database_exists(prefix))
            self.assertFalse(prefix.exists())

    def test_remove_database_lingering_file(self):
        with tempfile.TemporaryDirectory() as directory_pathname:
            prefix = Path(directory_pathname).joinpath("meh")
            io.add_database(prefix)
            prefix.joinpath("mah").touch()  # Add a file
            io.remove_database(prefix)
            self.assertFalse(io.database_exists(prefix))
            self.assertTrue(prefix.exists())
            prefix.joinpath("mah").is_file()  # File still exists

    def test_add_dataset(self):
        with tempfile.TemporaryDirectory() as directory_pathname:
            prefix = Path(directory_pathname)
            database = io.add_database(prefix)
            kind = "bike ride"
            unit = "km"
            self.assertFalse(database.dataset_exists(kind))
            dataset = database.add_dataset(kind, unit=unit)
            self.assertTrue(database.dataset_exists(kind))
            self.assertEqual(dataset.kind, kind)
            self.assertEqual(dataset.unit, unit)

    def test_remove_existing_dataset(self):
        with tempfile.TemporaryDirectory() as directory_pathname:
            prefix = Path(directory_pathname)
            database = io.add_database(prefix)
            kind = "bike ride"
            unit = "km"
            database.add_dataset(kind, unit=unit)
            self.assertTrue(database.dataset_exists(kind))
            database.remove_dataset(kind)
            self.assertFalse(database.dataset_exists(kind))

    def test_remove_non_existing_dataset(self):
        with tempfile.TemporaryDirectory() as directory_pathname:
            prefix = Path(directory_pathname)
            database = io.add_database(prefix)
            kind = "bike ride"
            with self.assertRaisesRegex(RuntimeError, "a dataset for kind"):
                database.remove_dataset(kind)
