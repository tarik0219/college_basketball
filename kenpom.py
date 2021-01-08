from datetime import datetime
from datetime import timedelta
from sportsreference.ncaab.boxscore import Boxscores
from sportsreference.ncaab.teams import Teams
import pandas as pd
import csv
import os
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from csv import reader
from csv import writer

map_names_not_same = {
                        "Alabama-Birmingham" : "UAB",
                        "Albany (NY)": "Albany",
                        "Arkansas-Pine Bluff" : "Arkansas Pine Bluff",
                        "Bethune-Cookman" : "Bethune Cookman",
                        "Bowling Green State" : "Bowling Green",
                        "Brigham Young" : "BYU",
                        "Cal State Bakersfield" : "Cal St. Bakersfield",
                        "Cal State Fullerton" : "Cal St. Fullerton",
                        "Cal State Northridge" : "Cal St. Northridge",
                        "California Baptist" : "Cal Baptist",
                        "UC-Davis" : "UC Davis",
                        "UC-Irvine" : "UC Irvine",
                        "UC-Riverside" : "UC Riverside",
                        "UCSB" : "UC Santa Barbara",
                        "University of California" : "California",
                        "Central Connecticut State" : "Central Connecticut",
                        "Central Florida" : "UCF",
                        "Citadel" : "The Citadel",
                        "College of Charleston" : "Charleston",
                        "Detroit Mercy" : "Detroit",
                        "Florida International" : "FIU",
                        "Gardner-Webb" : "Gardner Webb",
                        "Grambling" : "Grambling St.",
                        "Illinois-Chicago" : "Illinois Chicago",
                        "Purdue-Fort Wayne" : "Purdue Fort Wayne",
                        "Cal State Long Beach" : "Long Beach St.",
                        "Long Island University" : "LIU",
                        "Louisiana-Monroe" : "Louisiana Monroe",
                        "Louisiana State" : "LSU",
                        "Loyola (IL)" : "Loyola Chicago",
                        "Loyola (MD)" : "Loyola Marymount",
                        "Maryland-Baltimore County" : "UMBC",
                        "Maryland-Eastern Shore" : "Maryland Eastern Shore",
                        "Massachusetts-Lowell" : "UMass Lowell",
                        "Miami (FL)" : "Miami FL",
                        "Miami (OH)" : "Miami OH",
                        "Missouri-Kansas City" : "UMKC",
                        "Omaha" : "Nebraska Omaha",
                        "Nevada-Las Vegas" : "UNLV",
                        "North Carolina-Asheville" : "UNC Asheville",
                        "North Carolina-Greensboro" : "UNC Greensboro",
                        "North Carolina-Wilmington" : "UNC Wilmington",
                        "NC State" : "N.C. State",
                        "Pennsylvania" : "Penn",
                        "Prairie View" : "Prairie View A&M",
                        "Saint Francis (PA)" : "St. Francis PA",
                        "Saint Mary's (CA)" : "Saint Mary's",
                        "South Carolina Upstate" : "South Carolina St.",
                        "Southern California" : "USC",
                        "Southern Methodist" : "SMU",
                        "Southern Mississippi" : "Southern Miss",
                        "SIU-Edwardsville" : "SIU Edwardsville",
                        "St. Francis (NY)" : "St. Francis NY",
                        "St. John's (NY)" : "St. John's",
                        "Tennessee-Martin" : "Tennessee Martin",
                        "Texas A&M-Corpus Christi" : "Texas A&M Corpus Chris",
                        "Texas-Arlington" : "UT Arlington",
                        "Texas Christian" : "TCU",
                        "Texas-El Paso" : "UTEP",
                        "Texas-Rio Grande Valley" : "UT Rio Grande Valley",
                        "Texas-San Antonio" : "UTSA",
                        "Virginia Commonwealth" : "VCU",
                        "UConn" : "Connecticut",
                        "UMass-Lowell" : "UMass Lowell",
                        "UT-Martin" : "Tennessee Martin",
                        "UNC" : "North Carolina",
                        "Pitt" : "Pittsburgh"
                     }


def get_today():
    today = datetime.today()
    year = today.year
    month = today.month
    day = today.day
    return year,month,day

def get_yesterday():
    today = datetime.today()
    yesterday = today - timedelta(days = 1)
    year = yesterday.year
    month = yesterday.month
    day = yesterday.day
    return year,month,day

def get_games(year, month ,day):
    home_teams = []
    away_teams = []
    games = Boxscores(datetime(year, month, day))
    all_games = games.games[str(month)+'-'+str(day)+'-'+str(year)]
    for game in all_games:
        home_teams.append(game['home_name'])
        away_teams.append(game['away_name'])
        
    name = str(year)+"_"+str(month)+"_"+str(day)+"_games.csv"
    with open(name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["home_team","away_team"])
        for i,team in enumerate(home_teams):
            writer.writerow([home_teams[i],away_teams[i]])
            
    path = os.getcwd()
    os.rename(path+"\\"+name, path+"\\"+"games\\"+name)
    
    return home_teams,away_teams


def get_scores(year, month ,day):
    home_teams = []
    away_teams = []
    home_scores = []
    away_scores = []
    
    games = Boxscores(datetime(year, month, day))
    all_games = games.games[str(month)+'-'+str(day)+'-'+str(year)]
    
    for game in all_games:
        home_teams.append(game['home_name'])
        away_teams.append(game['away_name'])
        home_scores.append(game['home_score'])
        away_scores.append(game['away_score'])
    
    name = str(year)+"_"+str(month)+"_"+str(day)+"_scores.csv"
    with open(name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["home_team","away_team","home_score","away_score"])
        for i,team in enumerate(home_teams):
            writer.writerow([home_teams[i],away_teams[i],home_scores[i],away_scores[i]])
            
    path = os.getcwd()
    os.rename(path+"\\"+name, path+"\\"+"scores\\"+name)       
    return home_teams,away_teams,home_scores,away_scores

def kenpom(year, month ,day):
    options = webdriver.ChromeOptions() 
    #options.add_argument(r'''user-data-dir=C:\Users\Tarik's PC\AppData\Local\Google\Chrome\User Data''')
    #"user-data-dir=C:\Users\Tarik's PC\AppData\Local\Google\Chrome\User Data" home
    # "user-data-dir=C:\Users\koric1\AppData\Local\Google\Chrome\User Data" work
    #options.add_argument("--start-maximized")
    #self.options.add_argument("--headless")
    #self.options.add_argument("--no-sandbox")
    #self.options.add_argument("--disable-gpu")
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')  # Last I checked this was necessa
    driver = webdriver.Chrome(chrome_options= options)


    name = str(year)+"_"+str(month)+"_"+str(day)+"_kenpom.csv"

    with open(name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["team","off","def","tempo","luck"])
        #writer.writerow(["SN", "Name", "Contribution"])
        driver.get('https://kenpom.com/')
        time.sleep(1)

        for x in range(1,10):
            try:
                for z in range(1,41):

                    team_name = str(driver.find_element_by_xpath('//*[@id="ratings-table"]/tbody['+str(x)+']/tr['+str(z)+']/td[2]/a').text)
                    team_off = float(driver.find_element_by_xpath('//*[@id="ratings-table"]/tbody['+str(x)+']/tr['+str(z)+']/td[6]').text)
                    team_def = float(driver.find_element_by_xpath('//*[@id="ratings-table"]/tbody['+str(x)+']/tr['+str(z)+']/td[8]').text)
                    team_t = float(driver.find_element_by_xpath('//*[@id="ratings-table"]/tbody['+str(x)+']/tr['+str(z)+']/td[10]').text)
                    team_luck = float(driver.find_element_by_xpath('//*[@id="ratings-table"]/tbody['+str(x)+']/tr['+str(z)+']/td[12]').text)
                    #print(team_name,team_off,team_def,team_t,team_luck)
                    writer.writerow([team_name,team_off,team_def,team_t,team_luck])
            except:
                break
    path = os.getcwd()
    os.rename(path+"\\"+name, path+"\\"+"kenpom\\"+name)
    driver.close()
    
#combine for model
def score_kenmpom(year,month,day):
    path = os.getcwd() 
    scores = path+"\\scores\\"+str(year)+"_"+str(month)+"_"+str(day)+"_scores.csv"
    kenpom =  path+"\\kenpom\\"+str(year)+"_"+str(month)+"_"+str(day)+"_kenpom.csv"
    name = path+"\\scores_kenpom\\"+str(year)+"_"+str(month)+"_"+str(day)+"_scores_kenpom.csv"
    with open(name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["home","away","home_score","away_score","home_off","home_def","home_tempo","home_luck","away_off","away_def","away_tempo","away_luck"])
        with open(scores, 'r') as read_obj:
            csv_reader = reader(read_obj)
            header = next(csv_reader)
            if header != None:
                for row in csv_reader:
                    home_team = row[0]
                    away_team = row[1]
                    home_score = row[2]
                    away_score = row[3]

                    away_off = 0
                    away_def = 0
                    away_tempo = 0
                    away_luck = 0
                    
                    home_off = 0
                    home_def = 0
                    home_tempo = 0
                    home_luck = 0
                                    
                    

                    if home_team in map_names_not_same.keys():
                        home_team = map_names_not_same[home_team]
                    else:
                        name_list = home_team.split()
                        if name_list[-1] == "State":
                            name_list[-1] = "St."
                            new_name = " ".join(str(x) for x in name_list)
                            home_team = new_name
                        
                    
                    if away_team in map_names_not_same.keys():
                        away_team = map_names_not_same[away_team]
                    else:
                        name_list = away_team.split()
                        try:
                            if name_list[-1] == "State":
                                name_list[-1] = "St."
                                new_name = " ".join(str(x) for x in name_list)
                                away_team = new_name
                        except:
                            pass
                    
                    print(home_team, away_team)

                    with open(kenpom, 'r') as read_obj2:
                        csv_reader2 = reader(read_obj2)
                        header2 = next(csv_reader2)
                        if header2 != None:
                            for row2 in csv_reader2:
                                if row2[0] == home_team:
                                    home_off = row2[1]
                                    home_def = row2[2]
                                    home_tempo = row2[3]
                                    home_luck = row2[4]
                                    break
                    with open(kenpom, 'r') as read_obj2:
                        csv_reader2 = reader(read_obj2)
                        header2 = next(csv_reader2)
                        if header2 != None:
                            for row2 in csv_reader2:
                                if row2[0] == away_team:
                                    away_off = row2[1]
                                    away_def = row2[2]
                                    away_tempo = row2[3]
                                    away_luck = row2[4]
                                    break
                    if home_off == 0 or away_off == 0:
                        continue
                    writer.writerow([home_team,away_team,home_score,away_score,home_off,home_def,home_tempo,home_luck,away_off,away_def,away_tempo,away_luck])
      
#add to all 
def add_to_all(year,month,day):
    path = os.getcwd() 
    name = path+"\\scores_kenpom\\"+str(year)+"_"+str(month)+"_"+str(day)+"_scores_kenpom.csv"
    date = str(year)+"-"+str(month)+"-"+str(day)
    with open("all.csv", 'a+', newline='') as write_obj:
        csv_writer = writer(write_obj)
        with open(name, 'r') as read_obj:
            csv_reader = reader(read_obj)
            header = next(csv_reader)
            if header != None:
                for row in csv_reader:
                    print(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],date)
                    csv_writer.writerow([row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],date])    

def predict(year,month,day):
    path = os.getcwd() 
    games = path+"\\games\\"+str(year)+"_"+str(month)+"_"+str(day)+"_games.csv"
    name = path+"\\predict\\"+str(year)+"_"+str(month)+"_"+str(day)+"_predict.csv"
    kenpom = path+"\\kenpom\\"+str(year)+"_"+str(month)+"_"+str(day)+"_kenpom.csv"
    with open(name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["home","away","home_off","home_def","home_tempo","home_luck","away_off","away_def","away_tempo","away_luck"])
        with open(games, 'r') as read_obj:
            csv_reader = reader(read_obj)
            header = next(csv_reader)
            if header != None:
                for row in csv_reader:
                    home_team = row[0]
                    away_team = row[1]

                    away_off = 0
                    away_def = 0
                    away_tempo = 0
                    away_luck = 0
                    
                    home_off = 0
                    home_def = 0
                    home_tempo = 0
                    home_luck = 0
                

                    if home_team in map_names_not_same.keys():
                        home_team = map_names_not_same[home_team]
                    else:
                        name_list = home_team.split()
                        if name_list[-1] == "State":
                            name_list[-1] = "St."
                            new_name = " ".join(str(x) for x in name_list)
                            home_team = new_name
                        
                    
                    if away_team in map_names_not_same.keys():
                        away_team = map_names_not_same[away_team]
                    else:
                        name_list = away_team.split()
                        if name_list[-1] == "State":
                            name_list[-1] = "St."
                            new_name = " ".join(str(x) for x in name_list)
                            away_team = new_name


                    with open(kenpom, 'r') as read_obj2:
                        csv_reader2 = reader(read_obj2)
                        header2 = next(csv_reader2)
                        if header2 != None:
                            for row2 in csv_reader2:
                                if row2[0] == home_team:
                                    home_off = row2[1]
                                    home_def = row2[2]
                                    home_tempo = row2[3]
                                    home_luck = row2[4]
                                    break
                    with open(kenpom, 'r') as read_obj2:
                        csv_reader2 = reader(read_obj2)
                        header2 = next(csv_reader2)
                        if header2 != None:
                            for row2 in csv_reader2:
                                if row2[0] == away_team:
                                    away_off = row2[1]
                                    away_def = row2[2]
                                    away_tempo = row2[3]
                                    away_luck = row2[4]
                                    break
                    if home_off == 0 or away_off == 0:
                        continue
                    writer.writerow([home_team,away_team,home_off,home_def,home_tempo,home_luck,away_off,away_def,away_tempo,away_luck])

year,month,day = get_today()
kenpom(year, month ,day)
get_games(year, month ,day)
year,month,day = get_yesterday()
get_scores(year, month ,day)
score_kenmpom(year,month,day)
add_to_all(year,month,day)
year,month,day = get_today()
predict(year, month,day)
