import pandas as pd 
import rapidfuzz
import re
from datetime import datetime
import json



def add_surah(name):
    content = pd.read_csv("quran_tracker/quran.csv")

    if name not in content["Name"].values :
        new_ID = content["ID"].max()+1
        row = {
            "ID" : new_ID,
            "Name" : name,
            "Repetition" : 0,
            "Memorization" : 0,
            "date" :datetime.today().strftime("%d-%m-%Y") 
            }
                
        content = pd.concat([content , pd.DataFrame([row])],ignore_index=True)
        content.to_csv("quran_tracker/quran.csv", index=False)
        return True
    else :
        return False


def rev_surah(name,repetition):

    checked , rep , memo , datee = check_existence(name)
    old_progress = [rep , memo , datee]

    if  checked == True :
        last_date = datetime.today()
        datee = datetime.strptime(datee,'%d-%m-%Y')
            
        total_percentage , total_repetition = calculator(repetition , rep , memo , datee , last_date )
        
        content = pd.read_csv("quran_tracker/quran.csv")
        mask = content["Name"] == name

        content.loc[mask , ["Repetition"]] = int(total_repetition)
        content.loc[mask , ["Memorization"]] = int(total_percentage)
        content.loc[mask , ["date"]] = ((last_date.date()).strftime('%d-%m-%Y'))

        # add your data results in the csv file 
        content.to_csv("quran_tracker/quran.csv", index=False)


        return f"surat {name} is found ! \nYour repetition = {total_repetition} \nMemorization = {total_percentage}% \nLast date = {datee.date()}" , old_progress
        
        
    


def calculator (new_rep, old_rep , memo , old_date , new_date ):
    
    rep_total = int(new_rep) + int(old_rep)
    date_difference = (new_date- old_date).days

    per_total = abs(int(memo) + ((int(new_rep) * 4) / 5) - ((date_difference * 3) / 7)) 

    if per_total >= 100 :
        return 100 , rep_total
    else :
        return per_total , rep_total


def normelizer(name):
    return  re.sub("[, '\-_0-9!*$+°.?;:/§<>&é#\{\}=à@^ç\\|`è\[\]\(\)]","",name)

def match_surah(norm_surah):

    with open("quran_tracker/surahs.json","r") as file:
        surahs = json.load(file)
    
    norm_to_original = {normelizer(name).lower(): name for name in dict(surahs).values()}
    # extractOne searches through the normalized names (the keys of the choices dict)
    result = rapidfuzz.process.extract(
        norm_surah,
        norm_to_original.keys(),
        scorer=rapidfuzz.fuzz.WRatio,
        limit= 8
    )
    matched_surahs , percentages , ids  = list(zip(*result))

    for _ in range(len(matched_surahs)) :
        print(f"{norm_to_original[matched_surahs[_]]} : {percentages[_]}%")
    
    for _ in range(len(matched_surahs)) :
        if norm_surah == matched_surahs[_] and percentages[_] >= 65:
            return norm_to_original[matched_surahs[_]]


    
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
    

def verify_input(inpute):
    if len(inpute) >=3 :
        return inpute
    else : return False


def main():
    pass


if "__main__" == __name__ :
    main()