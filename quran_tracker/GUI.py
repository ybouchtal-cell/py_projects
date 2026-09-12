import customtkinter as ctk
import json
import quran_f
from Table import ShowTable


class window(ctk.CTk):
    def __init__(self):
        super().__init__()  # properly initializes the CTk machinery — self IS the window now

        self.geometry("600x400")
        self.title("Quran Tracker")

        self.label(text="Welcome to Habit tracker ! ", color="#00AEFF", padx=20, pady=20)

        self.button("Add Surah", self.AddSurah, 25, 25)
        self.button("Revision", self.rev_surah_gui, 27, 27)
        self.button("Daily Quests",self.Questes, 30, 30)
        self.button("Progress",ShowTable,100,40)


        self.mainloop()  # must be last — nothing after this line runs until the window closes

    def button(self, text, function, padx, pady):
        b = ctk.CTkButton(self, text=text, command=function)
        b.pack(padx=padx, pady=pady)

    def label(self, text, color, padx, pady):
        l = ctk.CTkLabel(self, text=text, text_color=color)
        l.pack(padx=padx, pady=pady)

    def AddSurah(self):
        sub_window(self)

    def rev_surah_gui(self):
        RevisionWindow(self)

    def Questes(self):
        QuestWindow(self)



class sub_window(ctk.CTkToplevel):
    def __init__(self, parent, *args, fg_color=None, **kwargs):
        super().__init__(*args, fg_color=fg_color, **kwargs)
 
        self.parent = parent  # reference back to the main window, if you need it later
 
        self.geometry("400x300")
        self.title("AddSurah")
 
        self.name = None  # will hold whatever the user has currently selected, updated live
        self.current_label = None
        self.saved = False

        self.create_label("Select your surah here !" , color="white" ,padx=45 ,pady=45)
 
        self.option_menu(width=150 , height=50 , padx=40 , pady=40 , values=self.read_surahs(),function=self.user_selection)
        # function=self.sub_success (NO parentheses) — pass a reference, don't call it now
        self.create_button(text="Enter", function=self.sub_success, padx=70, pady=50 , width=100 , height=50 , color=None)
        self.create_button(text="Undo", function=self.undo_progress, padx=80 , pady=50 , width=100 , height=50 ,color="red")
 
    def create_button(self, text, function, padx, pady , width , height , color):
        if color:
            b = ctk.CTkButton(self, text=text, command=function ,width=width , height=height , fg_color=color )
            b.pack(padx=padx, pady=pady)
        else :
            b = ctk.CTkButton(self, text=text, command=function ,width=width , height=height )
            b.pack(padx=padx, pady=pady)

    
 
    def create_label(self, text, color, padx, pady):
        if self.current_label is not None :
            self.current_label.pack_forget()

        self.current_label = ctk.CTkLabel(self, text=text, text_color=color )
        self.current_label.pack(padx=padx , pady=pady)
            
    def read_surahs(self):
        with open("quran_tracker/data/surahs.json", "r") as file:
            surahs = json.load(file)
        return list(surahs.values())
 
    def option_menu(self , width , height , padx , pady ,values , function ):
        self.options = ctk.CTkOptionMenu(
            self,
            values=values,
            command=function,
            width=width, 
            height=height 
        )  
        self.options.set("")
        self.options.pack(padx = padx , pady = pady)
 
    def user_selection(self, selected_value):
        self.name = selected_value
        print(f"selected value is ; {selected_value}")
 
    def sub_success(self ):
        # This only runs when Enter is actually clicked — the real "submit" moment. 

            if not self.name:
                self.create_label("No surah is selected yet !" , color="red" , padx=100 , pady=100 )
            else:
                print(f"is saved: {self.name}")
                self.saved=quran_f.add_surah(self.name)
                if self.saved :
                    self.create_label("Surah added Successfully !" , "green" , 100 , 100)
                else :
                    self.create_label("Surah is already saved !" , "yellow" , 100 , 100)
            

    def undo_progress(self):
        if self.saved :
            content = quran_f.read_csv()
            content = content.iloc[:-1]
            content.to_csv("quran_tracker/data/quran.csv", index=False)

            self.create_label("Surah is deleted !", "yellow" , 100 , 100)
        else :
            self.create_label("Enter a surah first !", "red" , 100 , 100)

class RevisionWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.title("Revision")
        self.geometry("400x300")

        self.current_label = None
        self.current_button = None
        self.old_process = []
        self.option_menu(width=150 , height=50 , padx=40 , pady=40 , values=self.read_submitions())

        self.entry = ctk.CTkEntry(self, placeholder_text="Enter number of repetition :")
        self.entry.pack(padx=20, pady=10)

        ctk.CTkButton(self, text="Submit", command=self.on_submit).pack(padx=20, pady=10)

    def option_menu(self , width , height , padx , pady ,values ):
            self.options = ctk.CTkOptionMenu(
                self,
                values=values,
                width=width, 
                height=height 
            )  
            self.options.set("")
            self.options.pack(padx = padx , pady = pady)
    
    def read_submitions(self):
        self.content = quran_f.read_csv()
        names = self.content.get("Name")
        return list(names)
    
    def on_submit(self):
        self.surah_enterd = self.options.get()
        surah_repition = self.entry.get()

        if surah_repition.isdigit() and not self.surah_enterd == "":
            if int(surah_repition) <= 100 :
                text , self.old_process =quran_f.rev_surah(name= self.surah_enterd , repetition= surah_repition)
                sub_window.create_label(self , text , "green" ,20 ,20)
                if not self.current_button :
                    ctk.CTkButton(self, text="Undo" , command=self.undo_submit).pack(padx=30 , pady=20)
                    self.current_button = True
            else :
                sub_window.create_label(self ,"ERROR:number is too big !" ,"red" ,20 ,20 )
        else :
            sub_window.create_label(self,"Enter a surah and number ! " , "red" , 20 , 20)

    def undo_submit(self) :
        mask = self.content["Name"] == self.surah_enterd
        self.content.loc[mask , ["Repetition" ,"Memorization" ,"date" ]] = int(self.old_process[0]) ,int(self.old_process[1]) ,self.old_process[2]
       

        self.content.to_csv("quran_tracker/data/quran.csv",index=False)

        sub_window.create_label(self ,"Progress is removed !" ,"yellow" ,20 ,20)


class QuestWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.title("Quests")
        self.geometry("400x300")

        self.current_label = None
        self.current_button = None
        self.old_process = []
        self.show_quests()
        self.option_menu( width=150 , height=50 , padx=40 , pady=40 , values=self.quest )
        self.entry()
        
        ctk.CTkButton(self ,  text="Submit", command=self.quests_adjust).pack(padx=20, pady=10)

    def show_quests(self):
            text , self.quest = quran_f.quests()
            sub_window.create_label(self , text , "white" ,20 ,20)
    
    def entry(self):
        self.choice=ctk.CTkEntry(self, placeholder_text="Enter number of repetition :")
        self.choice.pack(padx=20, pady=10)
    
    def option_menu(self , width , height , padx , pady ,values ):
            self.options = ctk.CTkOptionMenu(
                self,
                values=values,
                width=width, 
                height=height 
            )  
            self.options.set("")
            self.options.pack(padx = padx , pady = pady)
    
    def read_submitions(self):
        self.content = quran_f.read_csv()
        names = self.content.get("Name")
        return list(names)
    
    def quests_adjust(self):
            self.surah = self.options.get()
            self.adjustement = self.choice.get()
    
            if self.adjustement.isdigit() and not self.surah == "":
                text , self.old_progress = quran_f.rev_surah(self.surah , self.adjustement)
                sub_window.create_label(self , text , "green" ,20 ,20)
                if not self.current_button :
                    ctk.CTkButton(self, text="Undo" , command=self.undo_submit).pack(padx=30 , pady=20)
                    self.current_button = True
            elif self.adjustement > 100:
                    sub_window.create_label(self ,"ERROR:number is too big !" ,"red" ,20 ,20 )
            else :
                    sub_window.create_label(self,"Enter a surah and number ! " , "red" , 20 , 20)

    def undo_submit(self) :
        self.read_submitions()
        mask = self.content["Name"] == self.surah
        self.content.loc[mask , ["Repetition" ,"Memorization" ,"date" ]] = int(self.old_progress[0]) ,int(self.old_progress[1]) ,self.old_progress[2]
       

        self.content.to_csv("quran_tracker/data/quran.csv",index=False)

        sub_window.create_label(self ,"Progress is removed !" ,"yellow" ,20 ,20)





def main():
    window()


if __name__ == "__main__":
    main()