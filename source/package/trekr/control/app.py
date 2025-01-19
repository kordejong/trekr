import flet as ft
from . dataset_row import DatasetRow
from ..io import Database


# class App(DatasetRow):

class App(object):
    def __init__(self, page: ft.Page, databases: list[Database]):  # , store: DataStore):
        super().__init__()

        self.page = page
        # self.store: DataStore = store
        # self.page.on_route_change = self.route_change
        # self.boards = self.store.get_boards()
        # self.login_profile_button = PopupMenuItem(text="Log in", on_click=self.login)
        # self.appbar_items = [
        #     self.login_profile_button,
        #     PopupMenuItem(),  # divider
        #     PopupMenuItem(text="Settings"),
        # ]
        # self.appbar = AppBar(
        #     leading=Icon(icons.GRID_GOLDENRATIO_ROUNDED),
        #     leading_width=100,
        #     title=Text(f"Trolli", font_family="Pacifico", size=32, text_align="start"),
        #     center_title=False,
        #     toolbar_height=75,
        #     bgcolor=colors.LIGHT_BLUE_ACCENT_700,
        #     actions=[
        #         Container(
        #             content=PopupMenuButton(items=self.appbar_items),
        #             margin=margin.only(left=50, right=25),
        #         )
        #     ],
        # )
        # self.page.appbar = self.appbar
        # self.page.update()
        # super().__init__(
        #     self,
        #     self.page,
        #     self.store,
        #     tight=True,
        #     expand=True,
        #     vertical_alignment="start",
        # )

        self.dataset_row = DatasetRow(self.page, databases, expand=True)
        self.page.controls = [self.dataset_row]
        self.page.update()


    # # def build(self):
    # #     self.layout = DatasetRow(
    # #         self,
    # #         self.page,
    # #         self.store,
    # #         tight=True,
    # #         expand=True,
    # #         vertical_alignment="start",
    # #     )
    # #     return self.layout

    # def initialize(self):
    #     self.page.views.append(
    #         View(
    #             "/",
    #             [self.appbar, self],
    #             padding=padding.all(0),
    #             bgcolor=colors.BLUE_GREY_200,
    #         )
    #     )
    #     self.page.update()
    #     # create an initial board for demonstration if no boards
    #     if len(self.boards) == 0:
    #         self.create_new_board("My First Board")
    #     self.page.go("/")

    # def login(self, e):
    #     def close_dlg(e):
    #         if user_name.value == "" or password.value == "":
    #             user_name.error_text = "Please provide username"
    #             password.error_text = "Please provide password"
    #             self.page.update()
    #             return
    #         else:
    #             user = User(user_name.value, password.value)
    #             if user not in self.store.get_users():
    #                 self.store.add_user(user)
    #             self.user = user_name.value
    #             self.page.client_storage.set("current_user", user_name.value)

    #         dialog.open = False
    #         self.appbar_items[0] = PopupMenuItem(
    #             text=f"{self.page.client_storage.get('current_user')}'s Profile"
    #         )
    #         self.page.update()

    #     user_name = TextField(label="User name")
    #     password = TextField(label="Password", password=True)
    #     dialog = AlertDialog(
    #         title=Text("Please enter your login credentials"),
    #         content=Column(
    #             [
    #                 user_name,
    #                 password,
    #                 ElevatedButton(text="Login", on_click=close_dlg),
    #             ],
    #             tight=True,
    #         ),
    #         on_dismiss=lambda e: print("Modal dialog dismissed!"),
    #     )
    #     self.page.dialog = dialog
    #     dialog.open = True
    #     self.page.update()

    # def route_change(self, e):
    #     troute = TemplateRoute(self.page.route)
    #     if troute.match("/"):
    #         self.page.go("/boards")
    #     elif troute.match("/board/:id"):
    #         if int(troute.id) > len(self.store.get_boards()):
    #             self.page.go("/")
    #             return
    #         self.set_board_view(int(troute.id))
    #     elif troute.match("/boards"):
    #         self.set_all_boards_view()
    #     elif troute.match("/members"):
    #         self.set_members_view()
    #     self.page.update()

    # def add_board(self, e):
    #     def close_dlg(e):
    #         if (hasattr(e.control, "text") and not e.control.text == "Cancel") or (
    #             type(e.control) is TextField and e.control.value != ""
    #         ):
    #             self.create_new_board(dialog_text.value)
    #         dialog.open = False
    #         self.page.update()

    #     def textfield_change(e):
    #         if dialog_text.value == "":
    #             create_button.disabled = True
    #         else:
    #             create_button.disabled = False
    #         self.page.update()

    #     dialog_text = TextField(
    #         label="New Board Name", on_submit=close_dlg, on_change=textfield_change
    #     )
    #     create_button = ElevatedButton(
    #         text="Create", bgcolor=colors.BLUE_200, on_click=close_dlg, disabled=True
    #     )
    #     dialog = AlertDialog(
    #         title=Text("Name your new board"),
    #         content=Column(
    #             [
    #                 dialog_text,
    #                 Row(
    #                     [
    #                         ElevatedButton(text="Cancel", on_click=close_dlg),
    #                         create_button,
    #                     ],
    #                     alignment="spaceBetween",
    #                 ),
    #             ],
    #             tight=True,
    #         ),
    #         on_dismiss=lambda e: print("Modal dialog dismissed!"),
    #     )
    #     self.page.dialog = dialog
    #     dialog.open = True
    #     self.page.update()
    #     dialog_text.focus()

    # def create_new_board(self, board_name):
    #     new_board = Board(self, self.store, board_name, self.page)
    #     self.store.add_board(new_board)
    #     self.hydrate_all_boards_view()

    # def delete_board(self, e):
    #     self.store.remove_board(e.control.data)
    #     self.set_all_boards_view()
