import flet as ft
from chatcli import ChatClient
import os

TARGET_IP = os.getenv("SERVER_IP") or "127.0.0.1"
TARGET_PORT = os.getenv("SERVER_PORT") or "8889"
ON_WEB = os.getenv("ONWEB") or "0"


def main(page):
    page.title = "Chat App"
    is_login = False

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

    def retry_login(__e__):
        login_dialog()
        page.update()

    def login_click(__e__):
        if not username.value:
            username.error_text = "Please enter username"
            username.update()
        elif not password.value:
            password.error_text = "Please enter password"
            password.update()
        else:
            login = cc.login(username.value, password.value)

            if "Error" in login:
                page.dialog.title = ft.Text(
                    "Login Failed", style=ft.TextThemeStyle.TITLE_MEDIUM
                )
                page.dialog.content = ft.Text(login, style=ft.TextThemeStyle.BODY_SMALL)
                page.dialog.actions = [ft.ElevatedButton("Retry", on_click=retry_login)]
            else:
                username.value = ""
                password.value = ""
                is_login = True
                page.dialog.open = False

            page.update()

    def logout_click(__e__):
        is_login = False
        cc.logout()
        login_dialog()
        page.update()

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
            ft.PopupMenuItem(
                icon=ft.icons.LOGOUT, text="Logout", on_click=logout_click
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
