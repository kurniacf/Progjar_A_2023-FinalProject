import flet as ft
import json
from chatcli import ChatClient
import os

TARGET_IP = os.getenv("SERVER_IP") or "127.0.0.1"
TARGET_PORT = os.getenv("SERVER_PORT") or "8889"
ON_WEB = os.getenv("ONWEB") or "1"


class ChatList(ft.Container):
    def __init__(self, page, users, from_user):
        super().__init__()
        for value in users.values():
            print(value["username"])
        self.content = ft.Column(
            [
                ft.ListTile(
                    leading=ft.Icon(ft.icons.PERSON),
                    title=ft.Text(f"{value['username']}"),
                    on_click=lambda _: page.go(f"/private/{value['username']}"),
                )
                for value in users.values()
            ],
        )

        self.padding = ft.padding.symmetric(vertical=10)


class ChatRoom:
    def __init__(self, page, cc, from_user, to_user):
        self.chat = ft.TextField(
            label="Write a message...",
            autofocus=True,
            expand=True,
            on_submit=self.send_click,
        )
        self.lv = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
        self.send = ft.IconButton(
            icon=ft.icons.SEND_ROUNDED,
            tooltip="Send message",
            on_click=self.send_click,
        )
        self.file_picker = ft.FilePicker(on_result=self.upload_files, on_upload=self.upload_server)
        self.file_pick = ft.IconButton(
            icon=ft.icons.UPLOAD_FILE_ROUNDED,
            tooltip="Send file",
            on_click=self.on_pick_file,
        )
        self.page = page
        self.cc = cc
        self.from_user = from_user
        self.to_user = to_user
        self.page.pubsub.subscribe(self.on_chat)

    def on_pick_file(self, __e__):
        self.page.overlay.append(self.file_picker)
        self.page.update()
        self.file_picker.pick_files(allow_multiple=True)

    def send_click(self, __e__):
        if not self.chat.value:
            self.chat.error_text = "Please enter message"
            self.page.update()
        else:
            command = f"send {self.to_user} {self.chat.value}"
            server_call = self.cc.proses(command)
            self.lv.controls.append(ft.Text("To {}: {}".format(self.to_user, self.chat.value)))

            if "sent" in server_call:
                self.page.pubsub.send_all(self.chat.value)

            self.chat.value = ""
            self.chat.focus()
            self.page.update()

    def on_chat(self, message):
        check_inbox = json.loads(self.cc.inbox())
        self.lv.controls.append(ft.Text("From {}: {}".format(check_inbox[self.to_user][0]['msg_from'], check_inbox[self.to_user][0]['msg'])))
        self.page.update()

    # file picker and uploads
    def upload_files(self, e:ft.FilePickerResultEvent):
        upload_list = []
        if self.file_picker.result != None and self.file_picker.result.files != None:
            for f in self.file_picker.result.files:
                # print(self.page.get_upload_url(f.name, 600),)
                upload_list.append(
                    ft.FilePickerUploadFile(
                        f.name,
                        upload_url=self.page.get_upload_url(f.name, 600),
                    )
                )
            self.file_picker.upload(upload_list)
    
    def upload_server(self, e:ft.FilePickerUploadEvent):
        if(e.progress == 1):
            command = f"sendfile {self.to_user} app\\client\\upload\\{e.file_name}"
            print(command)
            server_call = self.cc.proses(command)
            print(server_call)

# menu_item_username = ft.PopupMenuItem(
#     icon=ft.icons.INSERT_EMOTICON, text="")

# is_login = False


def main(page):
    cc = ChatClient()
    page.title = "Chat App"
    is_login = False
    # def function_chain(*funcs):
    #     def chained_functions(*args, **kwargs):
    #         for func in funcs:
    #             func(*args, **kwargs)
    #     return chained_functions

    def login_dialog():
        # global is_login
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
        # global is_login
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
                # menu_item_username.text = "hallo bang, " + username.value
                username.value = ""
                password.value = ""
                username.error_text = ""
                password.error_text = ""
                is_login = True
                page.dialog.open = False
                # page.update()

            page.update()
            # page.update()

    def logout_click(__e__):
        # global is_login
        is_login = False
        cc.logout()
        login_dialog()
    #     dlg_modal.open = False
    #     page.update()
        
    # # logout modal
    # def close_dlg(e):
    #     dlg_modal.open = False
    #     page.update()
    
    # def logout_dlg(__e__):
    #     # global is_login
    #     is_login = False
    #     dlg_modal.open = False
    #     cc.logout()
    #     login_dialog()
    #     page.update()

    # def open_dlg_modal(e):
    #     page.dialog = dlg_modal
    #     dlg_modal.open = True
    #     page.update() 
    
    # dlg_modal = ft.AlertDialog(
    #     modal=True,
    #     title=ft.Text("Please confirm"),
    #     content=ft.Text("Do you really want to logout"),
    #     actions=[
    #         ft.TextButton("Yes", on_click=logout_click),
    #         ft.TextButton("No", on_click=close_dlg),
    #     ],
    #     actions_alignment=ft.MainAxisAlignment.END,
    #     on_dismiss=lambda e: print("Modal dialog dismissed!"),
    # )

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
            # menu_item_username,
            ft.PopupMenuItem(
                icon=ft.icons.LOGOUT, text="Logout", on_click=logout_click
                # icon=ft.icons.LOGOUT, text="Logout", on_click=open_dlg_modal
            ),
        ]
    )

    def route_change(__route__):
        troute = ft.TemplateRoute(page.route)
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

        if troute.match("/private"):
            page.views.append(
                ft.View(
                    "/private",
                    [
                        ft.AppBar(title=ft.Text("Private Chat"), actions=[menu]),
                        ft.Card(
                            content=ChatList(page, cc.info(), cc.username),
                        ),
                    ],
                )
            )

        elif troute.match("/private/:username"):
            cr = ChatRoom(page, cc, cc.username, troute.username)
            
            file_picker = ft.FilePicker()
            page.overlay.append(file_picker)
            page.update()

            page.views.append(
                ft.View(
                    f"/private/{troute.username}",
                    [
                        ft.AppBar(
                            title=ft.Text(f"Private Chat with {troute.username}"),
                            actions=[menu],
                        ),
                        cr.lv,
                        ft.Row([cr.chat, cr.send, cr.file_pick]),
                    ],
                )
            )

        elif troute.match("/group"):
            page.views.append(
                ft.View(
                    "/group",
                    [
                        ft.AppBar(title=ft.Text("Group Chat"), actions=[menu]),
                        # lv,
                        # ft.Row([chat, send]),
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
        ft.app(target=main, view=ft.WEB_BROWSER, port=8550, upload_dir="upload")
    else:
        ft.app(target=main)
