from pathlib import Path
import datetime
import sqlite3
import h5py


def adapt_time_point_iso(time_point: datetime.datetime) -> str:
    """Adapt datetime.datetime to timezone-naive ISO 8601 date."""
    return time_point.isoformat(timespec="minutes")


def convert_time_point(time_point: bytes) -> datetime.datetime:
    """Convert ISO 8601 datetime to datetime.datetime object."""
    return datetime.datetime.fromisoformat(time_point.decode("utf-8"))


sqlite3.register_adapter(datetime.datetime, adapt_time_point_iso)
sqlite3.register_converter("datetime", convert_time_point)


def meta_path(path: Path) -> Path:
    assert path.is_dir()

    return path.joinpath("meta.h5")


def record_path(path: Path) -> Path:
    assert path.is_dir()

    return path.joinpath("record.sqlite3")


class Dataset(object):

    def __init__(self, path: Path):

        assert path.is_dir(), path

        self.path = path

        with h5py.File(meta_path(path), "r") as file:
            self.kind = file.attrs["kind"]
            self.unit = file.attrs["unit"]


    def write(self, time_point: datetime.datetime, variant: str, magnitude: float) -> None:

        with sqlite3.connect(record_path(self.path), detect_types=sqlite3.PARSE_DECLTYPES) as connection:
            cursor = connection.cursor()

            results = cursor.execute("""
                SELECT variant from variants
            """)
            variants = results.fetchall()

            if not variant in variants:
                data = (
                    {
                        "variant_id": None,
                        "variant": variant,
                    },
                )
                cursor.executemany("INSERT INTO variants VALUES(:variant_id, :variant)", data)

            results = cursor.execute("""
                SELECT variant_id, variant from variants
            """)
            variant_ids, variants = tuple(map(list, zip(*results.fetchall())))
            variant_id = variant_ids[variants.index(variant)]

            data = (
                {
                    "magnitude_id": None,
                    "time_point": time_point,
                    "variant_id": variant_id,
                    "magnitude": magnitude,
                },
            )

            cursor.executemany("INSERT INTO magnitudes VALUES(:magnitude_id, :time_point, :variant_id, :magnitude)", data)


    def read(self) -> tuple[list[datetime.datetime], list[str], list[float]]:

        with sqlite3.connect(record_path(self.path), detect_types=sqlite3.PARSE_DECLTYPES) as connection:
            cursor = connection.cursor()

            results = cursor.execute("""
                SELECT time_point as [datetime], variant, magnitude
                FROM magnitudes
                INNER JOIN variants USING (variant_id)
            """)

            if records := results.fetchall():
                time_points, variants, magnitudes = tuple(map(list, zip(*records)))
            else:
                time_points, variants, magnitudes = [], [], []

        return time_points, variants, magnitudes



def initialize_dataset(path: Path, kind: str, unit: str) -> Dataset:

    assert path.is_dir()

    with h5py.File(meta_path(path), "w") as file:
        file.attrs["kind"] = kind
        file.attrs["unit"] = unit

    with sqlite3.connect(record_path(path)) as connection:
        cursor = connection.cursor()

        # variants: | variant_id | variant |
        cursor.execute("""
            CREATE TABLE variants(
                variant_id INTEGER PRIMARY KEY,
                variant TEXT NOT NULL UNIQUE
            )
        """)

        # magnitudes: | magnitude_id | time_point | variant_id | magnitude |
        cursor.execute("""
            CREATE TABLE magnitudes(
                magnitude_id INTEGER PRIMARY KEY,
                time_point datetime NOT NULL,
                variant_id INTEGER NOT NULL,
                magnitude REAL NOT NULL
            )
        """)

    return Dataset(path)


def clear_dataset(path: Path) -> None:

    assert path.is_dir()

    meta_path(path).unlink()
    record_path(path).unlink()


def contains_dataset(path: Path) -> bool:
    return path.is_dir() and meta_path(path).exists() and record_path(path).exists()
