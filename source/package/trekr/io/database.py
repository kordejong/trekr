import json
from pathlib import Path
from .dataset import Dataset, initialize_dataset, clear_dataset, contains_dataset
from .. import __version__


def normalize_kind(kind: str) -> str:
    # TODO
    return kind


def database_path(prefix: Path) -> Path:
    assert prefix.is_dir()

    return prefix.joinpath("trekr.json")


class Database(object):

    # Class for representing the current version of the database. Old versions first need to be upgraded.
    # A database contains references / mappings between dataset kind/variant and the dataset file. We could
    # also scan the file system for dataset files and obtain this info on the fly, but we want to be able to
    # maintain a custom ordering. NOTE: This could also be stored in an app-specific settings file, since this
    # info is only relevant for the list of datasets in the app.

    def __init__(self, prefix: Path):
        self.path = prefix

        with open(database_path(prefix), "r") as fp:
            self.trekr_object = json.load(fp)

        version = self.trekr_object["version"]
        assert version == __version__, f"{version} != {__version__}"

        # TODO Scan for datasets in the database's path - Think of a naming scheme for the dataset files:
        # <name>.trekr - How to name the files? <kind-variant>? Or some hash / random string? The name must be
        # representable in the file system. Maybe <kind-variant> with upper case letters lower cased and
        # spaces and dashes replaced by underscores, etc. The name doesn't matter. All relevant info is ready
        # from the dataset itself.

        # self.datasets: list[Dataset] = [Dataset(path) for path in self.path.glob("*-*.trekr")]

        self.datasets: list[Dataset] = [Dataset(path) for path in self.path.glob("*") if contains_dataset(path)]


    @property
    def version(self):
        return self.trekr_object["version"]


    def dataset_idx(self, kind: str) -> int:

        result = -1

        for idx, dataset in enumerate(self.datasets):
            if dataset.kind == kind:
                result = idx
                break

        assert result >= 0

        return result


    def dataset_exists(self, kind: str) -> bool:
        datasets = [dataset for dataset in self.datasets if dataset.kind == kind]
        assert 0 <= len(datasets) <= 1

        return len(datasets) == 1


    def add_dataset(self, kind: str, *, unit: str) -> Dataset:

        if self.dataset_exists(kind):
            raise RuntimeError(f"Cannot add dataset: a dataset for kind {kind} already exists")

        dataset_directory_name = f"{normalize_kind(kind)}"
        dataset_path = self.path.joinpath(dataset_directory_name)

        # Create the associated files
        dataset_path.mkdir()
        initialize_dataset(dataset_path, kind, unit)

        # Reference the dataset
        self.datasets.append(Dataset(dataset_path))

        return self.datasets[-1]


    def remove_dataset(self, kind: str) -> None:

        if not self.dataset_exists(kind):
            raise RuntimeError(f"Cannot remove dataset: a dataset for kind {kind} does not exist")

        dataset_directory_name = f"{normalize_kind(kind)}"
        dataset_path = self.path.joinpath(dataset_directory_name)

        # Dereference the dataset
        del self.datasets[self.dataset_idx(kind)]

        # Remove the associated files
        clear_dataset(dataset_path)
        dataset_path.rmdir()


def initialize_database(prefix: Path) -> None:

    if prefix.exists():
        if prefix.is_file():
            raise RuntimeError(f"Cannot initialize database: a regular file with name {prefix} already exists")
        elif prefix.is_dir():
            if len(list(prefix.iterdir())) > 0:
                raise RuntimeError(f"Cannot initialize database: directory with name {prefix} exists and is not empty")

    if not prefix.exists():
        prefix.mkdir()

    trekr_object = {"version": 0}

    with open(database_path(prefix), "w") as fp:
        json.dump(trekr_object, fp)


def upgrade_database_0_1(prefix: Path) -> None:

    with open(database_path(prefix), "r") as fp:
        trekr_object = json.load(fp)

    version = trekr_object["version"]
    assert version == 0, version
    trekr_object["version"] = version + 1
    trekr_object["datasets"] = []

    with open(database_path(prefix), "w") as fp:
        json.dump(trekr_object, fp)


def upgrade_database(prefix: Path) -> None:

    with open(database_path(prefix), "r") as fp:
        trekr_object = json.load(fp)

    database_version = trekr_object["version"]
    current_version = __version__

    # If database version is smaller than current version, make any necessary changes
    if database_version < current_version:
        if database_version == 0:
            upgrade_database_0_1(prefix)


def add_database(prefix: Path) -> Database:

    # - Initialize database, version 0
    # - Upgrade database to current version

    initialize_database(prefix)
    upgrade_database(prefix)

    return Database(prefix)


def database_exists(prefix: Path) -> bool:

    return prefix.is_dir() and database_path(prefix).is_file()


def remove_database(prefix: Path) -> None:

    if not database_exists(prefix):
        raise RuntimeError(f"Cannot remove database {prefix}: it doesn't seem to be a valid database")

    # Remove all files that we know are ours. If the resulting directory is empty, we can remove it entirely

    database = Database(prefix)

    for dataset in database.datasets:
        database.remove_dataset(dataset.kind)

    del database

    database_path(prefix).unlink()

    if len(list(prefix.iterdir())) == 0:
        prefix.rmdir()
