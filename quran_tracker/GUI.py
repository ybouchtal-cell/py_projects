import customtkinter as ctk
import json
import quran_f
from Table import ShowTable


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

ACCENT = "#00AEFF"
DANGER = "#E5484D"
SUCCESS = "#3DD68C"
WARNING = "#F5A623"
TEXT_MUTED = "#B5B5B5"

FONT_TITLE = ("Segoe UI", 22, "bold") #the big "📖 Quran Tracker" heading
FONT_SUBTITLE = ("Segoe UI", 15, "bold") #smaller bold headers inside each popup window ("Select a surah", "Log a revision")
FONT_BODY = ("Segoe UI", 13) #normal text: labels, entry placeholders, status messages
FONT_BUTTON = ("Segoe UI", 14, "bold") #bold text specifically for buttons, so they read as clickable

PAD_OUTER = 24 #the margin around the edge of each window's content (used as padx=PAD_OUTER, pady=PAD_OUTER on the outer frame)
PAD_WIDGET = 10 #the gap between individual widgets stacked inside a window (option menu, entry, etc.)
BTN_W, BTN_H = 220, 44 #size for the four main navigation buttons on the home screen (wide, since they're the primary actions)
BTN_W_SMALL, BTN_H_SMALL = 130, 40 #size for secondary buttons inside popups (Enter/Undo/Submit), which don't need to be as wide


class window(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("480x460")
        self.minsize(420, 420)
        self.title("Quran Tracker")

        # --- Header -------------------------------------------------------
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=PAD_OUTER, pady=(PAD_OUTER, 4))

        ctk.CTkLabel(
            header, text="📖 Quran Tracker", font=FONT_TITLE, text_color=ACCENT
        ).pack(anchor="center")

        ctk.CTkLabel(
            header,
            text="Track your memorization, revision and daily quests",
            font=FONT_BODY,
            text_color=TEXT_MUTED,
        ).pack(anchor="center", pady=(4, 0))

        ctk.CTkFrame(self, height=2, fg_color="#2B2B2B").pack(
            fill="x", padx=PAD_OUTER, pady=(16, 20)
        )

        # --- Action buttons -------------------------------------------------
        actions = ctk.CTkFrame(self, fg_color="transparent")
        actions.pack(expand=True, fill="both", padx=PAD_OUTER)

        self.nav_button(actions, "➕  Add Surah", self.AddSurah)
        self.nav_button(actions, "🔁  Revision", self.rev_surah_gui)
        self.nav_button(actions, "🎯  Daily Quests", self.Questes)
        self.nav_button(actions, "📊  Progress", ShowTable)

        self.mainloop()

    def nav_button(self, parent, text, function):
        b = ctk.CTkButton(
            parent,
            text=text,
            command=function,
            width=BTN_W,
            height=BTN_H,
            font=FONT_BUTTON,
            corner_radius=10,
        )
        b.pack(pady=PAD_WIDGET, fill="x")

    def AddSurah(self):
        sub_window(self)

    def rev_surah_gui(self):
        RevisionWindow(self)

    def Questes(self):
        QuestWindow(self)


class sub_window(ctk.CTkToplevel):
    def __init__(self, parent, *args, fg_color=None, **kwargs):
        super().__init__(*args, fg_color=fg_color, **kwargs)

        self.parent = parent
        self.geometry("380x340")
        self.title("Add Surah")
        self.resizable(False, False)

        self.name = None
        self.current_label = None
        self.saved = False

        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(expand=True, fill="both", padx=PAD_OUTER, pady=PAD_OUTER)

        ctk.CTkLabel(
            container, text="Select a surah", font=FONT_SUBTITLE
        ).pack(pady=(0, 4))

        self.status_area = ctk.CTkFrame(container, fg_color="transparent", height=30)
        self.status_area.pack(fill="x", pady=(0, 12))
        self.status_area.pack_propagate(False)

        self.option_menu(
            container, width=250, height=44, values=self.read_surahs(),
            function=self.user_selection,
        )

        btn_row = ctk.CTkFrame(container, fg_color="transparent")
        btn_row.pack(pady=(20, 0))

        self.create_button(
            btn_row, text="Enter", function=self.sub_success,
            width=BTN_W_SMALL, height=BTN_H_SMALL, color=None, side="left",
        )
        self.create_button(
            btn_row, text="Undo", function=self.undo_progress,
            width=BTN_W_SMALL, height=BTN_H_SMALL, color=DANGER, side="left",
        )

    def create_button(self, parent, text, function, width, height, color, side="top"):
        b = ctk.CTkButton(
            parent, text=text, command=function, width=width, height=height,
            font=FONT_BUTTON, corner_radius=8,
            fg_color=color if color else ctk.ThemeManager.theme["CTkButton"]["fg_color"],
        )
        b.pack(side=side, padx=8)

    def create_label(self, text, color, padx=0, pady=0):
        # padx/pady kept for backward compatibility with existing call sites
        target = self.status_area if hasattr(self, "status_area") else self
        if self.current_label is not None:
            self.current_label.destroy()

        self.current_label = ctk.CTkLabel(target, text=text, text_color=color, font=FONT_BODY)
        self.current_label.pack(pady=4)

    def read_surahs(self):
        with open("quran_tracker/data/surahs.json", "r") as file:
            surahs = json.load(file)
        return list(surahs.values())

    def option_menu(self, parent, width, height, values, function=None):
        self.options = ctk.CTkOptionMenu(
            parent,
            values=values,
            command=function,
            width=width,
            height=height,
            font=FONT_BODY,
            corner_radius=8,
        )
        self.options.set("Choose a surah")
        self.options.pack(pady=PAD_WIDGET)

    def user_selection(self, selected_value):
        self.name = selected_value

    def sub_success(self):
        if not self.name:
            self.create_label("No surah is selected yet !", color=DANGER)
        else:
            self.saved = quran_f.add_surah(self.name)
            if self.saved:
                self.create_label("Surah added successfully !", color=SUCCESS)
            else:
                self.create_label("Surah is already saved !", color=WARNING)

    def undo_progress(self):
        if self.saved:
            content = quran_f.read_csv()
            content = content.iloc[:-1]
            content.to_csv("quran_tracker/data/quran.csv", index=False)
            self.create_label("Surah deleted !", color=WARNING)
        else:
            self.create_label("Enter a surah first !", color=DANGER)


class RevisionWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.title("Revision")
        self.geometry("380x360")
        self.resizable(False, False)

        self.current_label = None
        self.current_button = None
        self.old_process = []

        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(expand=True, fill="both", padx=PAD_OUTER, pady=PAD_OUTER)

        ctk.CTkLabel(container, text="Log a revision", font=FONT_SUBTITLE).pack(pady=(0, 4))

        self.status_area = ctk.CTkFrame(container, fg_color="transparent", height=30)
        self.status_area.pack(fill="x", pady=(0, 12))
        self.status_area.pack_propagate(False)

        self.option_menu(container, width=250, height=44, values=self.read_submitions())

        self.entry = ctk.CTkEntry(
            container, placeholder_text="Number of repetitions", width=250, height=40,
            font=FONT_BODY, corner_radius=8,
        )
        self.entry.pack(pady=PAD_WIDGET)

        ctk.CTkButton(
            container, text="Submit", command=self.on_submit,
            width=BTN_W_SMALL, height=BTN_H_SMALL, font=FONT_BUTTON, corner_radius=8,
        ).pack(pady=(16, 0))

        self.button_slot = ctk.CTkFrame(container, fg_color="transparent")
        self.button_slot.pack(pady=(10, 0))

    def option_menu(self, parent, width, height, values):
        self.options = ctk.CTkOptionMenu(
            parent, values=values, width=width, height=height, font=FONT_BODY, corner_radius=8,
        )
        self.options.set("Choose a surah")
        self.options.pack(pady=PAD_WIDGET)

    def read_submitions(self):
        self.content = quran_f.read_csv()
        names = self.content.get("Name")
        return list(names)

    def on_submit(self):
        self.surah_enterd = self.options.get()
        surah_repition = self.entry.get()

        if surah_repition.isdigit() and not self.surah_enterd == "":
            if int(surah_repition) <= 100:
                text, self.old_process = quran_f.rev_surah(name=self.surah_enterd, repetition=surah_repition)
                sub_window.create_label(self, text, SUCCESS)
                if not self.current_button:
                    ctk.CTkButton(
                        self.button_slot, text="Undo", command=self.undo_submit,
                        width=BTN_W_SMALL, height=BTN_H_SMALL, fg_color=DANGER,
                        font=FONT_BUTTON, corner_radius=8,
                    ).pack()
                    self.current_button = True
            else:
                sub_window.create_label(self, "ERROR: number is too big !", DANGER)
        else:
            sub_window.create_label(self, "Enter a surah and number !", DANGER)

    def undo_submit(self):
        mask = self.content["Name"] == self.surah_enterd
        self.content.loc[mask, ["Repetition", "Memorization", "date"]] = (
            int(self.old_process[0]), int(self.old_process[1]), self.old_process[2]
        )
        self.content.to_csv("quran_tracker/data/quran.csv", index=False)
        sub_window.create_label(self, "Progress removed !", WARNING)


class QuestWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.title("Daily Quests")
        self.geometry("380x400")
        self.resizable(False, False)

        self.current_label = None
        self.current_button = None
        self.old_process = []

        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(expand=True, fill="both", padx=PAD_OUTER, pady=PAD_OUTER)

        ctk.CTkLabel(container, text="Today's Quest", font=FONT_SUBTITLE).pack(pady=(0, 4))

        self.status_area = ctk.CTkFrame(container, fg_color="transparent")
        self.status_area.pack(fill="x", pady=(0, 12))

        self.show_quests(self.status_area)
        self.option_menu(container, width=250, height=44, values=self.quest)
        self.entry(container)

        ctk.CTkButton(
            container, text="Submit", command=self.quests_adjust,
            width=BTN_W_SMALL, height=BTN_H_SMALL, font=FONT_BUTTON, corner_radius=8,
        ).pack(pady=(16, 0))

        self.button_slot = ctk.CTkFrame(container, fg_color="transparent")
        self.button_slot.pack(pady=(10, 0))

    def show_quests(self, parent):
        text, self.quest = quran_f.quests()
        ctk.CTkLabel(parent, text=text, text_color="white", font=FONT_BODY, wraplength=280).pack()

    def entry(self, parent):
        self.choice = ctk.CTkEntry(
            parent, placeholder_text="Number of repetitions", width=250, height=40,
            font=FONT_BODY, corner_radius=8,
        )
        self.choice.pack(pady=PAD_WIDGET)

    def option_menu(self, parent, width, height, values):
        self.options = ctk.CTkOptionMenu(
            parent, values=values, width=width, height=height, font=FONT_BODY, corner_radius=8,
        )
        self.options.set("Choose a surah")
        self.options.pack(pady=PAD_WIDGET)

    def read_submitions(self):
        self.content = quran_f.read_csv()
        names = self.content.get("Name")
        return list(names)

    def quests_adjust(self):
        self.surah = self.options.get()
        self.adjustement = self.choice.get()

        if self.adjustement.isdigit() and not self.surah == "":
            text, self.old_progress = quran_f.rev_surah(self.surah, self.adjustement)
            sub_window.create_label(self, text, SUCCESS)
            if not self.current_button:
                ctk.CTkButton(
                    self.button_slot, text="Undo", command=self.undo_submit,
                    width=BTN_W_SMALL, height=BTN_H_SMALL, fg_color=DANGER,
                    font=FONT_BUTTON, corner_radius=8,
                ).pack()
                self.current_button = True
        elif self.adjustement.isdigit() and int(self.adjustement) > 100:
            sub_window.create_label(self, "ERROR: number is too big !", DANGER)
        else:
            sub_window.create_label(self, "Enter a surah and number !", DANGER)

    def undo_submit(self):
        self.read_submitions()
        mask = self.content["Name"] == self.surah
        self.content.loc[mask, ["Repetition", "Memorization", "date"]] = (
            int(self.old_progress[0]), int(self.old_progress[1]), self.old_progress[2]
        )
        self.content.to_csv("quran_tracker/data/quran.csv", index=False)
        sub_window.create_label(self, "Progress removed !", WARNING)


def main():
    window()


if __name__ == "__main__":
    main()