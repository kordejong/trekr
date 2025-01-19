from pathlib import Path
# from trekr.flet.dataset_drawer import DatasetDrawer
import trekr
import flet as ft
import tempfile
import trekr


databases: list[trekr.Database] = []


def create_dummy_databases():
    tmp_path = Path(tempfile.gettempdir()).joinpath("trekr")

    owncloud_prefix = tmp_path.joinpath("owncloud", "trekr")

    if trekr.database_exists(owncloud_prefix):
        trekr.remove_database(owncloud_prefix)

    database = trekr.add_database(owncloud_prefix)
    databases.append(database)
    kind = "bike ride"
    variant = "Gazelle Paris"
    description = "My bike rides with my Gazelle Paris"
    unit = "km"
    dataset = database.add_dataset(kind, variant=variant, description=description, unit=unit)

    icloud_prefix = tmp_path.joinpath("icloud", "trekr")

    if trekr.database_exists(icloud_prefix):
        trekr.remove_database(icloud_prefix)

    database = trekr.add_database(icloud_prefix)
    databases.append(database)
    kind = "bike ride"
    variant = "idWorkx oPinion"
    description = "My bike rides with my idWorkx oPinion"
    unit = "km"
    dataset = database.add_dataset(kind, variant=variant, description=description, unit=unit)

    local_prefix = tmp_path.joinpath("local", "trekr")

    if trekr.database_exists(local_prefix):
        trekr.remove_database(local_prefix)

    database = trekr.add_database(local_prefix)
    databases.append(database)
    kind = "weight"
    variant = "body"
    description = "My body weight"
    unit = "kg"
    dataset = database.add_dataset(kind, variant=variant, description=description, unit=unit)


def main(page: ft.Page):

    ### # def handle_dataset_drawer_dismissal(event):
    ### #     pass

    ### def handle_dataset_selection(event):
    ###     # page.add(ft.Text(f"Selected Index changed: {event.control.selected_index}"))
    ###     page.close(drawer)

    ### drawer = DatasetDrawer(databases, on_change=handle_dataset_selection)


    ### #     # TODO Make custom control:
    ### #     #      - row with:
    ### #     #          - drawer | button | content

    ### page.add(ft.ElevatedButton("Select dataset", on_click=lambda event: page.open(drawer)))




    page.title = "Trekr"
    # page.padding = 0
    # page.theme = theme.Theme(font_family="Verdana")
    # page.theme.page_transitions.windows = "cupertino"
    # page.fonts = {"Pacifico": "Pacifico-Regular.ttf"}
    # page.bgcolor = colors.BLUE_GREY_200
    app = trekr.App(page, databases)  # , InMemoryStore())
    # page.add(app)
    # page.update()
    # app.initialize()


create_dummy_databases()
ft.app(main)





# def select_database(database_idx):
#     database = databases[database_idx]

#     # page.horizontal_alignment = ft.CrossAxisAlignment.CENTER


#     # def handle_dismissal(event):
#     #     page.add(ft.Text("Drawer dismissed"))


#     def handle_dataset_selected(event):
#         # page.add(ft.Text(f"Selected Index changed: {event.control.selected_index}"))
#         page.close(drawer)

#     drawer = DatasetDrawer(database.datasets, on_change=handle_dataset_selected)

#     # drawer = ft.NavigationDrawer(
#     #     # on_dismiss=handle_dismissal,
#     #     on_change=handle_change,
#     #     controls = [
#     #         ft.NavigationDrawerDestination(
#     #             label=f"{dataset.kind}\n{dataset.variant}",
#     #             icon=ft.Icons.DOOR_BACK_DOOR_OUTLINED,
#     #             selected_icon=ft.Icon(ft.Icons.DOOR_BACK_DOOR),
#     #         ) for dataset in database.datasets
#     #     ],
#     # )

#     # TODO Turn this into an icon
#     # TODO hier verder:
#     # TODO Make database ѕelector something which can be hidden
#     # TODO Make custom control:
#     #      - row with:
#     #          - drawer | button | content
#     tabs.tabs[database_idx].content = ft.ElevatedButton("Select dataset", on_click=lambda event: page.open(drawer))


# def handle_database_selected(event):
#     # TODO Cache idx of selected dataset by database idx. Switching databases should not reset dataset
#     #      idxs.
#     database_idx = int(event.data)
#     select_database(database_idx)
#     # page.add(ft.Text(f"Database selected {database.path}"))



# database_idx = 0

# tabs = ft.Tabs(
#     selected_index=database_idx,
#     animation_duration=300,
#     tabs = [
#         ft.Tab(
#             text=f"{database.path}",
#             icon=ft.Icons.DATASET,
#             content=ft.Container(
#                 # TODO Show currently selected dataset
#                 # content=ft.Text(f"This is Tab {idx}"),
#                 # alignment=ft.alignment.center,
#             ),
#         ) for idx, database in enumerate(databases)
#     ],
#     expand=1,
#     on_change=handle_database_selected,
# )

# select_database(database_idx)
# page.add(tabs)



# import flet as ft


# def main(page: ft.Page):
#     counter = ft.Text("0", size=50, data=0)
#
#     def increment_click(e):
#         counter.data += 1
#         counter.value = str(counter.data)
#         counter.update()
#
#     page.floating_action_button = ft.FloatingActionButton(
#         icon=ft.Icons.ADD, on_click=increment_click
#     )
#     page.add(
#         ft.SafeArea(
#             ft.Container(
#                 counter,
#                 alignment=ft.alignment.center,
#             ),
#             expand=True,
#         )
#     )
#
#
# ft.app(main)


