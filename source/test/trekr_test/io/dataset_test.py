from pathlib import Path
import datetime
import tempfile
import unittest

from trekr import io


class DatasetTest(unittest.TestCase):

    def test_add_record(self):
        with tempfile.TemporaryDirectory() as directory_pathname:
            prefix = Path(directory_pathname)
            database = io.add_database(prefix)
            kind = "bike ride"
            unit = "km"
            dataset = database.add_dataset(kind, unit=unit)

            time_points_read, variants_read, distances_read = dataset.read()
            self.assertEqual(time_points_read, [])
            self.assertEqual(variants_read, [])
            self.assertEqual(distances_read, [])

            now = datetime.datetime.now(datetime.timezone.utc)

            time_point_written = datetime.datetime(now.year, now.month, now.day, now.hour, now.minute)
            variant_written = "Gazelle Paris"
            distance_written = 55.5
            dataset.write(time_point_written, variant_written, distance_written)

            time_points_read, variants_read, distances_read = dataset.read()

            self.assertEqual(len(time_points_read), 1)
            self.assertEqual(len(variants_read), 1)
            self.assertEqual(len(distances_read), 1)

            self.assertEqual(time_points_read[0], time_point_written)
            self.assertEqual(variants_read[0], variant_written)
            self.assertEqual(distances_read[0], distance_written)
