import datetime
import flet as ft
from . dataset_drawer import DatasetDrawer
from . dataset_tabs import DatasetTabs
from ..io import Database


class DatasetRow(ft.Row):

    def __init__(self, page: ft.Page, databases: list[Database], *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.page = page
        self.drawer = DatasetDrawer(databases, on_change=self.handle_select_dataset)
        self.date_picker = ft.DatePicker(
            first_date=datetime.datetime(year=2000, month=1, day=1),
            last_date=datetime.datetime(year=2049, month=12, day=31),
            on_change=self.handle_date_picked)
        self.time_picker = ft.TimePicker(on_change=self.handle_time_picked)
        # TODO self.magnitude_picker = ft.TimePicker(on_change=self.handle_time_picked)
        self.button = ft.ElevatedButton("Select dataset", on_click=lambda event: self.page.open(self.drawer))
        self.controls = [self.button]
        self.time_point: datetime.datetime = datetime.datetime.now(datetime.timezone.utc)
        self.magnitude: float = 0.0



        # self.app = app
        # self.page = page
        # self.page.on_resize = self.page_resize
        # self.store: DataStore = store
        # self.toggle_nav_rail_button = IconButton(
        #     icon=icons.ARROW_CIRCLE_LEFT,
        #     icon_color=colors.BLUE_GREY_400,
        #     selected=False,
        #     selected_icon=icons.ARROW_CIRCLE_RIGHT,
        #     on_click=self.toggle_nav_rail,
        # )
        # self.sidebar = Sidebar(self, self.store, page)
        # self.members_view = Text("members view")
        # self.all_boards_view = Column(
        #     [
        #         Row(
        #             [
        #                 Container(
        #                     Text(value="Your Boards", style="headlineMedium"),
        #                     expand=True,
        #                     padding=padding.only(top=15),
        #                 ),
        #                 Container(
        #                     TextButton(
        #                         "Add new board",
        #                         icon=icons.ADD,
        #                         on_click=self.app.add_board,
        #                         style=ButtonStyle(
        #                             bgcolor={
        #                                 "": colors.BLUE_200,
        #                                 "hovered": colors.BLUE_400,
        #                             },
        #                             shape={"": RoundedRectangleBorder(radius=3)},
        #                         ),
        #                     ),
        #                     padding=padding.only(right=50, top=15),
        #                 ),
        #             ]
        #         ),
        #         Row(
        #             [
        #                 TextField(
        #                     hint_text="Search all boards",
        #                     autofocus=False,
        #                     content_padding=padding.only(left=10),
        #                     width=200,
        #                     height=40,
        #                     text_size=12,
        #                     border_color=colors.BLACK26,
        #                     focused_border_color=colors.BLUE_ACCENT,
        #                     suffix_icon=icons.SEARCH,
        #                 )
        #             ]
        #         ),
        #         Row([Text("No Boards to Display")]),
        #     ],
        #     expand=True,
        # )
        # self._active_view: Control = self.all_boards_view

        # self.controls = [self.sidebar, self.toggle_nav_rail_button, self.active_view]

    # @property
    # def active_view(self):
    #     return self._active_view

    # @active_view.setter
    # def active_view(self, view):
    #     self._active_view = view
    #     self.controls[-1] = self._active_view
    #     self.sidebar.sync_board_destinations()
    #     self.update()

    ### # def handle_dataset_drawer_dismissal(event):
    ### #     pass


    def handle_select_dataset(self, event):
        self.page.close(self.drawer)

        self.dataset = self.drawer.datasets[event.control.selected_index]
        self.dataset_tabs = DatasetTabs(self.dataset, expand=True)
        self.controls = [
            self.button,
            ft.Column(
                controls=[
                    self.dataset_tabs,
                    ft.FloatingActionButton(icon=ft.Icons.ADD, on_click=self.handle_add_record),
                ],
                expand=True,
            ),
        ]
        self.update()


    def handle_date_picked(self, event):
        self.time_point = datetime.datetime.fromisoformat(event.data)
        self.page.open(self.time_picker)


    def handle_time_picked(self, event):
        time = datetime.time.fromisoformat(event.data + ":00")
        self.time_point = self.time_point.replace(hour=time.hour, minute=time.minute)

        # TODO hier verder
        # self.page.open(self.magnitude_picker)


    def handle_magnitude_picked(self, event):
        print(event)
        self.new_magnitude = float(event.data)

        self.dataset.write(self.time_point, self.magnitude)
        self.dataset_tabs.handle_add_record()


    def handle_add_record(self, event):
        self.page.open(self.date_picker)

        # self.page.overlay = [
        #     ft.TextField(
        #         # placeholder_text="Only numbers are allowed",
        #         input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9]*$", replacement_string="")
        #     )
        #     ]

        # self.page.update



        # def main(page: ft.Page):
        #     text = ft.Text()
        #
        #     def change_text(e):
        #         # Filter out non-numeric characters
        #         value = ''.join(filter(str.isdigit, e.control.value))
        #         e.control.value = value
        #         text.value = value
        #         page.update()
        #
        #     page.add(
        #         ft.Column(
        #             [
        #                 ft.TextField(
        #                     label="Number Input",
        #                     keyboard_type=ft.KeyboardType.NUMBER,
        #                     on_change=change_text,
        #                 ),
        #                 text,
        #             ]
        #         )
        #     )
        #
        # ft.app(target=main)





    # def set_board_view(self, i):
    #     self.active_view = self.store.get_boards()[i]
    #     self.sidebar.bottom_nav_rail.selected_index = i
    #     self.sidebar.top_nav_rail.selected_index = None
    #     self.sidebar.update()
    #     self.page.update()
    #     self.page_resize()

    # def set_all_boards_view(self):
    #     self.active_view = self.all_boards_view
    #     self.hydrate_all_boards_view()
    #     self.sidebar.top_nav_rail.selected_index = 0
    #     self.sidebar.bottom_nav_rail.selected_index = None
    #     self.sidebar.update()
    #     self.page.update()

    # def set_members_view(self):
    #     self.active_view = self.members_view
    #     self.sidebar.top_nav_rail.selected_index = 1
    #     self.sidebar.bottom_nav_rail.selected_index = None
    #     self.sidebar.update()
    #     self.page.update()

    # def page_resize(self, e=None):
    #     if type(self.active_view) is Board:
    #         self.active_view.resize(
    #             self.sidebar.visible, self.page.width, self.page.height
    #         )
    #     self.page.update()

    # def hydrate_all_boards_view(self):
    #     self.all_boards_view.controls[-1] = Row(
    #         [
    #             Container(
    #                 content=Row(
    #                     [
    #                         Container(
    #                             content=Text(value=b.name),
    #                             data=b,
    #                             expand=True,
    #                             on_click=self.board_click,
    #                         ),
    #                         Container(
    #                             content=PopupMenuButton(
    #                                 items=[
    #                                     PopupMenuItem(
    #                                         content=Text(
    #                                             value="Delete",
    #                                             style="labelMedium",
    #                                             text_align="center",
    #                                         ),
    #                                         on_click=self.app.delete_board,
    #                                         data=b,
    #                                     ),
    #                                     PopupMenuItem(),
    #                                     PopupMenuItem(
    #                                         content=Text(
    #                                             value="Archive",
    #                                             style="labelMedium",
    #                                             text_align="center",
    #                                         ),
    #                                     ),
    #                                 ]
    #                             ),
    #                             padding=padding.only(right=-10),
    #                             border_radius=border_radius.all(3),
    #                         ),
    #                     ],
    #                     alignment="spaceBetween",
    #                 ),
    #                 border=border.all(1, colors.BLACK38),
    #                 border_radius=border_radius.all(5),
    #                 bgcolor=colors.WHITE60,
    #                 padding=padding.all(10),
    #                 width=250,
    #                 data=b,
    #             )
    #             for b in self.store.get_boards()
    #         ],
    #         wrap=True,
    #     )
    #     self.sidebar.sync_board_destinations()

    # def board_click(self, e):
    #     self.sidebar.bottom_nav_change(self.store.get_boards().index(e.control.data))

    # def toggle_nav_rail(self, e):
    #     self.sidebar.visible = not self.sidebar.visible
    #     self.toggle_nav_rail_button.selected = not self.toggle_nav_rail_button.selected
    #     self.page_resize()
    #     self.page.update()
