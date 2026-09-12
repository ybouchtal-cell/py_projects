
import pandas as pd 
import rapidfuzz
import re
from datetime import datetime
import json
from quran_f import DATA_FILE, read_csv


def add_surah():
    new_surah = verify_input( input("enter surah : "))

    if new_surah == False :
        print("Type a surah that exists ! ")
        return

    norm_surah = normelizer(new_surah)
    best_match = match_surah(norm_surah)

    if check_existence(best_match) :
        print("surah already exist  !") 
    else :
        content = read_csv()
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
        
        content.to_csv(DATA_FILE, index=False)
        print("surah added successfully !")
        

def rev_surah():

    surah = input("enter the surah that ur revising :").lower().strip()
    norm_surah = normelizer(surah)
    match = match_surah(norm_surah)

    if not match :
        print(f"can't match any surah !\nTry in another typing method !")
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
        
        content = read_csv()
        mask = content["Name"] == match

        content.loc[mask , ["Repetition"]] = int(total_repetition)
        content.loc[mask , ["Memorization"]] = int(total_percentage)
        content.loc[mask , ["date"]] = ((last_date.date()).strftime('%d-%m-%Y'))

        # add your data results in the csv file 
        content.to_csv(DATA_FILE, index=False)
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
    content = read_csv()

    if surah == None :
        return False , False , False ,False
    
    else :
        if surah in content["Name"].values :
            datee =content.loc[content['Name'] == surah , 'date'].squeeze() 
            return True , content.loc[content['Name'] == surah , 'Repetition'].squeeze() , content.loc[content['Name'] == surah , 'Memorization'].squeeze() , datee
        else :
            return False 

def quests():
    content = read_csv()
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
    print("Welcome to the quran tracker\nTell me what do you want to do today ?\n")
    while True :
        print("-->Memorize a new surah (m).\n-->Revision (r).\n-->Give you a quest(q).\n-->exit(e)")
        choice = input("Enter your choice : ")
        match choice :
            case("m") :
                add_surah()
            case("r"):
                rev_surah()
            case("q"):
                quests()
            case("e"):
                break
           


                
    


if __name__ == "__main__":
    main()