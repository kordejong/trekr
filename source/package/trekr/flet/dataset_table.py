import datetime
import flet as ft


class TimePointCell(ft.DataCell):

    def __init__(self, time_point, *args, **kwargs):
        super().__init__(ft.Text(f"{time_point}"), *args, **kwargs)

        # if self.show_edit_icon:
        #     self.on_tap = self.handle_on_tab

    # def handle_on_tab(self, event):
    #     print("edit time point")
    #     print(event)
    #     # TODO Replace cell with something like this:
    #     # ft.TextField(
    #     # placeholder_text="Only numbers are allowed",
    #     # input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9]*$", replacement_string="")
    #     # )


class MagnitudeCell(ft.DataCell):

    def __init__(self, magnitude, *args, **kwargs):
        super().__init__(ft.Text(f"{magnitude}"), *args, **kwargs)

        # if self.show_edit_icon:
        #     self.on_tap = self.handle_on_tab

    # def handle_on_tab(self, event):
    #     print("edit magnitude")
    #     print(event)
    #     # TODO Replace cell with something like this:
    #     # ft.TextField(
    #     # placeholder_text="Only numbers are allowed",
    #     # input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9]*$", replacement_string="")
    #     # )


class DatasetTable(ft.DataTable):

    def __init__(self, dataset, *args, **kwargs):

        columns = [
            ft.DataColumn(ft.Text("Date")),
            ft.DataColumn(ft.Text("Magnitude"), numeric=True),
        ]

        super().__init__(columns=columns, *args, **kwargs)

        self.dataset = dataset

        self.recreate_table()


    def recreate_table(self):
        time_points, magnitudes = self.dataset.read()
        self.rows = [
            ft.DataRow(
                cells=[
                    TimePointCell(time_point),
                    MagnitudeCell(magnitude),
                ]) for time_point, magnitude in zip(time_points, magnitudes)
        ]


    def handle_add_record(self):
        self.recreate_table()
        self.update()
