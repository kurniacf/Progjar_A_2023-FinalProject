import flet as ft
from chatcli import ChatClient
import os

TARGET_IP = os.getenv("SERVER_IP") or "127.0.0.1"
TARGET_PORT = os.getenv("SERVER_PORT") or "8889"
ON_WEB = os.getenv("ONWEB") or "0"

menu_item_username = ft.PopupMenuItem(
    icon=ft.icons.INSERT_EMOTICON, text="")

is_login = False


def main(page):
    page.title = "Chat App"

    def function_chain(*funcs):
        def chained_functions(*args, **kwargs):
            for func in funcs:
                func(*args, **kwargs)
        return chained_functions

    def btn_click(__e__):
        if not chat.value:
            chat.error_text = "masukkan command"
            page.update()
        else:
            txt = chat.value
            lv.controls.append(ft.Text(f"command: {txt}"))
            txt = cc.proses(txt)
            lv.controls.append(ft.Text(f"result {cc.tokenid}: {txt}"))
            chat.value = ""
            page.update()

    def login_dialog():
        global is_login
        page.dialog = ft.AlertDialog(
            open=not is_login,
            modal=True,
            title=ft.Text(
                "Welcome! Please login first", style=ft.TextThemeStyle.TITLE_MEDIUM
            ),
            content=ft.Column([username, password], tight=True),
            actions=[ft.ElevatedButton("Login", on_click=login_click)],
            actions_alignment="end",
        )

    def login_click(__e__):
        global is_login
        if not username.value:
            username.error_text = "Please enter username"
            username.update()
        elif not password.value:
            password.error_text = "Please enter password"
            password.update()
        else:
            login = cc.login(username.value, password.value)

            if "Error" in login:
                username.error_text = "Username or Password does not match"
                password.error_text = "Username or Password does not match"
                username.update()

            else:
                menu_item_username.text = "hallo bang, " + username.value
                username.value = ""
                password.value = ""
                username.error_text=""
                password.error_text =""
                is_login = True
                page.dialog.open = False
                page.update()

            page.update()
            page.update()

    def logout_click(__e__):
        global is_login
        is_login = False
        cc.logout()
        login_dialog()
        dlg_modal.open = False
        page.update()
        
    # logout modal
    def close_dlg(e):
        dlg_modal.open = False
        page.update()
    
    def logout_dlg(__e__):
        global is_login
        is_login = False
        dlg_modal.open = False
        cc.logout()
        login_dialog()
        page.update()

    def open_dlg_modal(e):
        page.dialog = dlg_modal
        dlg_modal.open = True
        page.update() 
    
    dlg_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Please confirm"),
        content=ft.Text("Do you really want to logout"),
        actions=[
            ft.TextButton("Yes", on_click=logout_click),
            ft.TextButton("No", on_click=close_dlg),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
        on_dismiss=lambda e: print("Modal dialog dismissed!"),
    )

    cc = ChatClient()

    lv = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
    chat = ft.TextField(label="Write a message...", autofocus=True, expand=True, on_submit=btn_click)
    send = ft.ElevatedButton("Send", on_click=btn_click)

    username = ft.TextField(label="Username", autofocus=True)
    password = ft.TextField(
        label="Password",
        password=True,
        can_reveal_password=True,
        autofocus=True,
        on_submit=login_click,
    )
    
    login_dialog()

    menu = ft.PopupMenuButton(
        items=[
            menu_item_username,
            ft.PopupMenuItem(
                # icon=ft.icons.LOGOUT, text="Logout", on_click=logout_click
                icon=ft.icons.LOGOUT, text="Logout", on_click=open_dlg_modal
            ),
        ]
    )

    def route_change(__route__):
        page.views.clear()
        page.views.append(
            ft.View(
                "/",
                [
                    menu,
                    ft.Card(
                        content=ft.Container(
                            content=ft.Column(
                                [
                                    ft.ListTile(
                                        leading=ft.Icon(ft.icons.PERSON),
                                        title=ft.Text("Private Chat"),
                                        on_click=lambda _: page.go("/private"),
                                    ),
                                    ft.ListTile(
                                        leading=ft.Icon(ft.icons.GROUP),
                                        title=ft.Text("Group Chat"),
                                        on_click=lambda _: page.go("/group"),
                                    ),
                                ],
                            ),
                            padding=ft.padding.symmetric(vertical=10),
                        )
                    ),
                ],
            )
        )

        if page.route == "/private":
            page.views.append(
                ft.View(
                    "/private",
                    [
                        ft.AppBar(title=ft.Text("Private Chat"), actions=[menu]),
                        lv,
                        ft.Row([chat, send]),
                    ],
                )
            )

        if page.route == "/group":
            page.views.append(
                ft.View(
                    "/group",
                    [
                        ft.AppBar(title=ft.Text("Group Chat"), actions=[menu]),
                        lv,
                        ft.Row([chat, send]),
                    ],
                )
            )
        page.update()

    def view_pop(__view__):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


if __name__ == "__main__":
    if ON_WEB == "1":
        ft.app(target=main, view=ft.WEB_BROWSER, port=8550)
    else:
        ft.app(target=main)
