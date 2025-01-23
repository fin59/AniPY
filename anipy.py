import json
import tkinter as tk
import webbrowser
from contextlib import nullcontext

import requests
from PIL import Image, ImageTk


with open('client_secrets.json')as secrets:
    secret=json.load(secrets)
    client_id = secret['client_id']
    client_secret = secret['client_secret']
    redirect_uri = 'http://localhost/callback'
    auth_url = f'https://anilist.co/api/v2/oauth/authorize?client_id={client_id}&response_type=token'
    token_url = 'https://anilist.co/api/v2/oauth/token'
    api_url='https://graphql.anilist.co'


class AppGUI:
    def __init__(self):
        self.root=tk.Tk()
        self.root.geometry("1200x800")
        self.root.title("AniPY")
        self.anilist_api = AnilistAPI(self)

        self.nav_bar=tk.Frame(self.root,background="#101424", width=400)
        self.nav_bar.pack(side="left", fill="y")
        self.main_panel=tk.Frame(self.root,background="#182434")
        self.main_panel.pack(side="right", fill="both",expand=True)

        self.menu_options = ["Strona Główna", "Szukaj", "Profil", "Zaloguj Się"]
        for option in self.menu_options:
            button=tk.Button(self.nav_bar,text=option,font=("Arial", 22),bg="#101424",fg="white",relief="flat", command=lambda opt=option: self.change_main_panel(opt))
            button.pack(fill="x",pady=10)
        self.change_main_panel(self.menu_options[0])

        self.root.mainloop()

    def change_main_panel(self, option):
        for widget in self.main_panel.winfo_children():
            widget.destroy()

        if option == "Strona Główna":
            label = tk.Label(self.main_panel, text="Strona Główna", font=("Arial", 20), bg="#182434",
                             fg="white")
            label.pack(pady=20)
            self.home_scrollable_frame = tk.Frame(self.main_panel, bg="#182434")
            self.home_scrollable_frame.pack(fill="both", expand=True)

            #self.scrollbar = tk.Scrollbar(self.home_scrollable_frame)
            #self.scrollbar.pack(side="right", fill="y")
            #self.scrollbar.config(command=self.home_scrollable_frame.yview)

            self.anilist_api.load_trending_anime()
        elif option == "Szukaj":
            print()
        elif option == "Profil":
            print()
        elif option == "Zaloguj Się":
            print()

    def display_anime(self, title, image_url):
        frame = tk.Frame(self.home_scrollable_frame, relief="ridge", borderwidth=2, bg="#101424")
        frame.pack(pady=5, padx=10, fill="x")

        try:
            response = requests.get(image_url, stream=True, timeout=10)
            if response.status_code == 200:
                image = Image.open(response.raw).resize((80, 100), Image.LANCZOS)
                image = ImageTk.PhotoImage(image)

                image_label = tk.Label(frame, image=image, bg="#101424")
                image_label.image = image
                image_label.pack(side="left", padx=10)
        except Exception:
            image_label = tk.Label(frame, text="[Obrazek niedostępny]", bg="#101424", fg="white")
            image_label.pack(side="left", padx=10)

        title_label = tk.Label(frame, text=title, wraplength=200, justify="left", bg="#101424", fg="white",
                               font=("Arial", 12))
        title_label.pack(side="left", fill="x", padx=10)


class AnilistAPI:
    def __init__(self, app_gui):
        self.app_gui = app_gui

    def get_token(self):
        webbrowser.open(auth_url)
        token = input("kod:")
        access_token = token.split("access_token=")[1].split("&")[0]
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        return headers

    def load_trending_anime(self):
        query = """
                query {
                  Page(page: 1, perPage: 10) {
                    media(type: ANIME, sort: TRENDING_DESC) {
                      id
                      title {
                        romaji
                      }
                      coverImage {
                        large
                      }
                    }
                  }
                }
                """
        response = requests.post(api_url, json={"query": query})
        if response.status_code == 200:
            data = response.json()
            for anime in data["data"]["Page"]["media"]:
                title = anime["title"]["romaji"]
                image_url = anime["coverImage"]["large"]
                self.app_gui.display_anime(title, image_url)


if __name__ == "__main__":
    AppGUI()