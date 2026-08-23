
import pandas as pd 
import rapidfuzz
import re
from datetime import datetime
surahs = {
    1: "Al-Fatihah",
    2: "Al-Baqarah",
    3: "Al-Imran",
    4: "An-Nisa",
    5: "Al-Ma'idah",
    6: "Al-An'am",
    7: "Al-A'raf",
    8: "Al-Anfal",
    9: "At-Tawbah",
    10: "Yunus",
    11: "Hud",
    12: "Yusuf",
    13: "Ar-Ra'd",
    14: "Ibrahim",
    15: "Al-Hijr",
    16: "An-Nahl",
    17: "Al-Isra",
    18: "Al-Kahf",
    19: "Maryam",
    20: "TaHa",
    21: "Al-Anbiya",
    22: "Al-Hajj",
    23: "Al-Mu'minun",
    24: "An-Nur",
    25: "Al-Furqan",
    26: "Ash-Shu'ara",
    27: "An-Naml",
    28: "Al-Qasas",
    29: "Al-Ankabut",
    30: "Ar-Rum",
    31: "Luqman",
    32: "As-Sajdah",
    33: "Al-Ahzab",
    34: "Saba",
    35: "Fatir",
    36: "Ya-Sin",
    37: "As-Saffat",
    38: "Sad",
    39: "Az-Zumar",
    40: "Ghafir",
    41: "Fussilat",
    42: "Ash-Shura",
    43: "Az-Zukhruf",
    44: "Ad-Dukhan",
    45: "Al-Jathiyah",
    46: "Al-Ahqaf",
    47: "Muhammad",
    48: "Al-Fath",
    49: "Al-Hujurat",
    50: "Qaf",
    51: "Adh-Dhariyat",
    52: "At-Tur",
    53: "An-Najm",
    54: "Al-Qamar",
    55: "Ar-Rahman",
    56: "Al-Waqi'ah",
    57: "Al-Hadid",
    58: "Al-Mujadilah",
    59: "Al-Hashr",
    60: "Al-Mumtahanah",
    61: "As-Saff",
    62: "Al-Jumu'ah",
    63: "Al-Munafiqun",
    64: "At-Taghabun",
    65: "At-Talaq",
    66: "At-Tahrim",
    67: "Al-Mulk",
    68: "Al-Qalam",
    69: "Al-Haqqah",
    70: "Al-Ma'arij",
    71: "Nuh",
    72: "Al-Jinn",
    73: "Al-Muzzammil",
    74: "Al-Muddaththir",
    75: "Al-Qiyamah",
    76: "Al-Insan",
    77: "Al-Mursalat",
    78: "An-Naba",
    79: "An-Nazi'at",
    80: "Abasa",
    81: "At-Takwir",
    82: "Al-Infitar",
    83: "Al-Mutaffifin",
    84: "Al-Inshiqaq",
    85: "Al-Buruj",
    86: "At-Tariq",
    87: "Al-A'la",
    88: "Al-Ghashiyah",
    89: "Al-Fajr",
    90: "Al-Balad",
    91: "Ash-Shams",
    92: "Al-Layl",
    93: "Ad-Duha",
    94: "Ash-Sharh",
    95: "At-Tin",
    96: "Al-Alaq",
    97: "Al-Qadr",
    98: "Al-Bayyinah",
    99: "Az-Zalzalah",
    100: "Al-Adiyat",
    101: "Al-Qari'ah",
    102: "At-Takathur",
    103: "Al-Asr",
    104: "Al-Humazah",
    105: "Al-Fil",
    106: "Quraysh",
    107: "Al-Ma'un",
    108: "Al-Kawthar",
    109: "Al-Kafirun",
    110: "An-Nasr",
    111: "Al-Masad",
    112: "Al-Ikhlas",
    113: "Al-Falaq",
    114: "An-Nas"
}

def add_surah():
    new_surah = input("enter surah : ")
    norm_surah = normelizer(new_surah)
    best_match = match_surah(norm_surah)

    if check_existence(best_match) :
        print("surah already exist  !") 
    else :
        content = pd.read_csv("quran_tracker/quran.csv")
        new_ID = content["ID"].max()+1

        row = {
            "ID" : new_ID,
            "Name" : best_match,
            "Repetition" : 0,
            "Memorization" : 0,
            "date" :datetime.today().strftime("%d-%m-%Y") 
        }

        #pd.dataframe is used to transform the row Dict into a row dataframe
        #then i used pd.concat to add the new row dataframe 
        # ignore_index is for creating a new sequential index instead of having to row with same index
        
        
        content = pd.concat([content , pd.DataFrame([row])],ignore_index=True)

        #to_csv is used to save the csv file 
        
        content.to_csv("quran_tracker/quran.csv", index=False)
        print("surah added successfully !")
        
def speaker(name) :
    print(f"hello {name} !\n I'm your personal habit tracker for quran ! ")
    while True :
        choice = input("have u memorized a new surah today or just a small revision ?\n choose (memo\rev) :" )
        if choice.lower() == "memo" :
            add_surah()
            False
        elif choice.lower() == "rev" :
            rev_surah()
            False
        else :
            print("choose (memo\rev) !")

def rev_surah():

    surah = input("enter the surah that ur revising :").lower().strip()
    norm_surah = normelizer(surah)
    match = match_surah(norm_surah)

    if not match :
        print(f"can't match surah {match}\nTry in another typing method !")
        return

    checked , rep , memo , datee = check_existence(match)

    if  checked == True :
        print(f"surat {match} is found ! \nYour repetition = {rep} \nMemorization = {memo}% \nLast date = {datee}")

        last_date = datetime.today()
        datee = datetime.strptime(datee,'%d-%m-%Y')

        while True:
            try :
               repetition =int(input(f"how many times did you repeat surah {match} "))
               break
            except ValueError :
                print("Enter the number of repetition (expecting a integer value) ")
            
                

        total_percentage , total_repetition = calculator(repetition , rep , memo , datee , last_date )
        
        content = pd.read_csv("quran_tracker/quran.csv")
        mask = content["Name"] == match

        content.loc[mask , ["Repetition"]] = int(total_repetition)
        content.loc[mask , ["Memorization"]] = int(total_percentage)
        content.loc[mask , ["date"]] = ((last_date.date()).strftime('%d-%m-%Y'))

        # add your data results in the csv file 
        content.to_csv("quran_tracker/quran.csv", index=False)
        print(f"Your progress is added to surah {match} !")

    else :
        print(f"surah {match} is not saved yet ! ")


def calculator (new_rep, old_rep , memo , old_date , new_date ):
    
    rep_total = int(new_rep) + int(old_rep)
    date_difference = (new_date- old_date).days

    per_total = abs(int(memo) + ((int(new_rep) * 4) / 5) - ((date_difference * 3) / 7)) 

    return per_total , rep_total


def normelizer(name):
    return  re.sub("[, '\-_0-9!*$+°.?;:/§<>&é#\{\}=à@^ç\\|`è\[\]\(\)]","",name)

def match_surah(norm_surah):
    
    norm_to_original = {normelizer(name).lower(): name for name in surahs.values()}
    print(norm_to_original)
    # extractOne searches through the normalized names (the keys of the choices dict)
    result = rapidfuzz.process.extract(
        norm_surah,
        norm_to_original.values(),
        scorer=rapidfuzz.fuzz.WRatio,
        limit= 8
    )
    matched_surahs , percentages , ids  = list(zip(*result))
    print(f"the normelized surah : {norm_surah}")
    print(f"matched surahs are {matched_surahs}")
    print(f"percentages {percentages}")
    found = False
    
    for _ in range(len(matched_surahs)) :
        if norm_surah == normelizer(matched_surahs[_]).lower() or percentages[_] >= 80:
            found = True
            print(f"fond surah : {matched_surahs[_]}")
            return matched_surahs[_]

    if not found :
        return False

    
def  check_existence(surah):
    content = pd.read_csv("quran_tracker/quran.csv")

    if surah == None :
        return False , False , False ,False
    
    else :
        if surah in content["Name"].values :
            datee =content.loc[content['Name'] == surah , 'date'].squeeze() 
            return True , content.loc[content['Name'] == surah , 'Repetition'].squeeze() , content.loc[content['Name'] == surah , 'Memorization'].squeeze() , datee
        else :
            return False 

def quests():
    content = pd.read_csv("quran_tracker/quran.csv")
    print(content)
    memo = list(content.get("Memorization"))
    surahs = list(content.get("Name")) 
    dates = list(content.get("date"))
    quest = {
        "name": [],
        "percentage" : [],
        "date" : []
    }

    for surah in range(len(surahs)):
            if memo[surah] <= 50 :
                quest["name"].append(surahs[surah])
                quest["percentage"].append(memo[surah])
                quest["date"].append(dates[surah])

    print(quest)
    
    if len(quest["name"]) != 0 :
        print("these are the following list for today : \n ")
        for _ in range(len(quest["name"])) :
            print(f"{quest["name"][_]} percentage: {quest["percentage"][_]}% since {quest["date"][_]}")
    else :
        print("no quest found for today !")
    
    




    
    



def main():
    print("Welcome to the quran tracker\nTell me what do you want to do today ?\n")
    while True :
        print("-->Memorize a new surah (m).\n-->Revision (r).\n-->Give you a quest(q).")
        choice = input("Enter your choice : ")
        match choice :
            case("m") :
                add_surah()
                break
            case("r"):
                rev_surah()
                break
            case("q"):
                quests()
            case("exit"):
                break
           


                
    


if __name__ == "__main__":
    main()