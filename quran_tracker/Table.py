import customtkinter as ctk
import quran_f


class ShowTable(ctk.CTk):
    def __init__(self, fg_color = None, **kwargs):
        super().__init__(fg_color, **kwargs)

        self.geometry("900x500")
        self.title("Progress Table")

        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both",expand=True,padx=20,pady=20)

        self.label = ctk.CTkLabel(self.main_frame,text="Quran Progress",font=ctk.CTkFont(size=24,weight="bold"))
        self.label.pack(pady=(20,0))

        self.create_table()


        self.mainloop()

    def create_table(self):
        content = quran_f.read_csv()

        table_frame = ctk.CTkFrame(
            self ,
            fg_color="#1e1e1e" ,
            corner_radius=10
        )
        table_frame.pack(
            fill="both",
            expand=True ,
            padx=20 ,
            pady=20
        )

        columns = content.columns.to_list()

        for column_number , column_name in enumerate(columns):
            header = ctk.CTkLabel(
                table_frame ,
                text=column_name,
                font = ctk.CTkFont(size=14 , weight ="bold"),
                fg_color="#2b2b2b",
                corner_radius=5
            )
            header.grid(
                row = 0,
                column =column_number ,
                padx=2 ,
                pady=2,
                sticky = "nsew"
            )

        for row_number, (_, row) in enumerate(content.iterrows(), start=1):
            for column_number, value in enumerate(row):
                cell = ctk.CTkLabel(
                    table_frame,
                    text=str(value),
                    font=ctk.CTkFont(size=13),
                    fg_color="#242424",                            corner_radius=3
                    )

                cell.grid(
                    row=row_number,
                    column=column_number,
                    padx=2,
                    pady=2,
                    sticky="nsew"
                    )
        for column_number in range(len(columns)):
            table_frame.grid_columnconfigure(
            column_number,
            weight=1
        )




def main():
    ShowTable()

if __name__ == "__main__" :
    main()