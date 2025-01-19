from ..io import Database, Dataset
import flet as ft


class DatasetDrawerDestination(ft.NavigationDrawerDestination):

    def __init__(self, dataset: Dataset):
        super().__init__()

        self.label=f"{dataset.kind}"  # \n{dataset.variant}"
        # icon=ft.Icons.DOOR_BACK_DOOR_OUTLINED
        # selected_icon=ft.Icon(ft.Icons.DOOR_BACK_DOOR)


class DatasetDrawer(ft.NavigationDrawer):

    # Allow the user to select a dataset. Once a dataset is selected, call user-provided on-change.

    def __init__(self, databases: list[Database], *, on_dismiss=None, on_change=None):
        super().__init__()

        self.on_dismiss=on_dismiss
        self.on_change=on_change

        self.controls = []
        self.datasets = []

        for database_idx, database in enumerate(databases):
            self.controls.append(ft.Text(f"{database.path}"))

            for dataset in database.datasets:
                self.controls.append(DatasetDrawerDestination(dataset))
                self.datasets.append(dataset)

            if database_idx != len(databases) - 1:
                self.controls.append(ft.Divider(thickness=2))
