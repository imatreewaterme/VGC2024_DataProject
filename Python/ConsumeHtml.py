import sys
import numpy
import csv
import pandas as pd
import fnmatch
import requests
from bs4 import BeautifulSoup
import numpy as np
#Functions#
def stringParse(string):
    string = string.replace(' -', "")
    string = string.replace('- ', "")
    return string

def clearDictionary():
    emptyDictionary = {
    "pokemon":"",
    "helditem":"",
    "ability":"",
    "type":"",
    "move1":"",
    "move2":"",
    "move3":"",
    "move4":"",
    "rank":""
            }
    return emptyDictionary
###############
with open('SourceHTML/vgcData.html') as file:
    soup = BeautifulSoup(file, 'html.parser')
pokemonTeams = []
for link in soup.find_all('a'):
    href =link.get('href')
    if (fnmatch.fnmatch(str(href), "*pokepast.es*")):
        pokemonTeams.append(str(href))

pokemonDict = clearDictionary()
field_names=["pokemon","helditem","ability","type","move1","move2","move3","move4","rank"]

with open('../csvFiles/data.csv', 'a') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames = field_names)
    writer.writeheader()

ranking = 0
for team in pokemonTeams:
    ranking+=1
    r = requests.get(team)
    soup2 = BeautifulSoup(r.text, "html.parser")
    nextFlag = False
    itemFlag = False
    for pokemon in soup2.find_all('article'):
        i = 0    
        for string in pokemon.stripped_strings:
            #DATA ISSUE with value "Urshifu" we need to parse it differently
            if(len(string)>50):
                string = string.split("\r\n")
                for value in string:
                    value = stringParse(value)
                    if ('@' in value):
                        if(value == "@"):
                            itemFlag = True
                        elif(' @ ' in value):
                            result = value.split(' @ ')
                        elif('@ ' in value):
                            result = value.split('@ ')
                        #Use result to handle special case here for the item and pokemon on one line
                        if(len(result)==2):
                            pokemonDict["pokemon"] = result[0].strip()
                            pokemonDict["helditem"] = result[1].strip()
                            itemFlag = False
                        else:
                            print("Error cannot split pokemon name and held item")
                    elif("Ability: " in value):
                        result = value.split('Ability: ')
                        pokemonDict["ability"] = result[1].strip()
                    elif("Tera Type: " in value): 
                        result = value.split('Tera Type: ')
                        pokemonDict["type"] = result[1].strip()
                    else:
                        for key in pokemonDict.keys(): 
                            if pokemonDict[key]=="":
                                pokemonDict[key]=value.strip()
                                break
                pokemonDict["rank"] = ranking
                with open('../csvFiles/data.csv', 'a') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames = field_names)
                    writer.writerow(pokemonDict)
            else:
                string = stringParse(string)
                if(itemFlag):
                    pokemonDict["helditem"]=string
                    string=""
                    itemFlag= False
                if((string != "") and (string!="-")):
                    i+=1
                    if ('@' in string):
                        if(i == 1):#string is in incorrect format of "Pokemon @ HeldItem"
                            if(' @ ' in string):
                                result = string.split(' @ ')
                            elif('@ ' in string):
                                result = string.split('@ ')
                            #Use result to handle special case here for the item and pokemon on one line
                            if(len(result)==2):
                                pokemonDict["pokemon"] = result[0]
                                pokemonDict["helditem"] = result[1]
                                itemFlag = False
                        if(string=='@'):#Item
                            itemFlag = True
                        elif(string[0]=='@'):#Item
                            pokemonDict["helditem"]=string.replace('@ ',"")
                            itemFlag = False
                    else:
                        if(i==1):#Pokemon
                            pokemonDict["pokemon"]=string
                        elif(string =="Ability:") or (string == "Tera Type:"):#Ignore this string and adjust flag for next string
                            nextFlag = True
                        elif(nextFlag == True):
                            if("\n" in string):
                                values = string.split("\n")
                                pokemonDict["type"]=values[0].strip()
                                pokemonDict["move1"]=values[1].strip()
                                nextFlag = False
                            elif(pokemonDict["ability"]==""):
                                pokemonDict["ability"]=string
                                nextFlag = False
                            else:
                                pokemonDict["type"]=string
                                nextFlag = False
                        else:
                            #check for multiline
                            if("\n" in string):
                                moves = string.split("\n")
                                for value in moves:
                                    if(value=="-"):
                                        value = ""
                                    value = value.strip()
                                    if(pokemonDict["move1"]==""):
                                        pokemonDict["move1"]=value

                                    elif(pokemonDict["move2"]==""):
                                        pokemonDict["move2"]=value

                                    elif(pokemonDict["move3"]==""):
                                        pokemonDict["move3"]=value

                                    elif(pokemonDict["move4"]==""):
                                        pokemonDict["move4"]=value
                                
                            else:
                                if(string=="-"):
                                    string = ""
                                if(pokemonDict["move1"]==""):
                                    pokemonDict["move1"]=string

                                elif(pokemonDict["move2"]==""):
                                    pokemonDict["move2"]=string

                                elif(pokemonDict["move3"]==""):
                                    pokemonDict["move3"]=string

                                elif(pokemonDict["move4"]==""):
                                    pokemonDict["move4"]=string

                pokemonDict["rank"]=ranking
        print(repr(pokemonDict))
        with open('../csvFiles/data.csv', 'a') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames = field_names)
            writer.writerow(pokemonDict)
        pokemonDict = clearDictionary()