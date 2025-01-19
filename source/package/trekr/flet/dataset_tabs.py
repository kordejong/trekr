import flet as ft
from .dataset_plot import DatasetPlot
from .dataset_table import DatasetTable
from ..io import Dataset


class DatasetTabs(ft.Tabs):

    def __init__(self, dataset: Dataset, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.dataset = dataset
        self.table = DatasetTable(self.dataset)
        self.plot = DatasetPlot(self.dataset)

        # selected_index=database_idx,
        # animation_duration=300,
        # tabs = [
        #     ft.Tab(
        #         text=f"{database.path}",
        #         icon=ft.Icons.DATASET,
        #         content=ft.Container(
        #             # TODO Show currently selected dataset
        #             # content=ft.Text(f"This is Tab {idx}"),
        #             # alignment=ft.alignment.center,
        #         ),
        #     ) for idx, database in enumerate(databases)
        # ],
        # on_change=handle_database_selected,

        self.tabs = [
            ft.Tab(
                text="Records",
                icon=ft.Icons.DATASET,
                content=self.table,
                # content=ft.Container(
                #     # TODO Show currently selected dataset
                #     content=ft.Text(f"Records: {self.dataset.kind} / {self.dataset.variant}"),
                #     # alignment=ft.alignment.center,
                # ),

                # content=ft.Column(
                #     controls=[
                #         DatasetTable(self.dataset),
                #         ft.FloatingActionButton(icon=ft.Icons.ADD, on_click=self.handle_add_record),
                #     ],
                # ),
            ),
            ft.Tab(
                text="Graph",
                icon=ft.Icons.SCATTER_PLOT,
                content=self.plot,
                # content=ft.Container(
                #     # TODO Show currently selected dataset
                #     content=ft.Text(f"Graph: {self.dataset.kind} / {self.dataset.variant}"),
                #     # alignment=ft.alignment.center,
                # ),
            ),
        ]

    def handle_add_record(self):
        self.table.handle_add_record()
        self.plot.handle_add_record()
