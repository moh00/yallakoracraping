from bs4 import BeautifulSoup
import csv
import requests
import datetime
from tkinter import Label
from main import root
def scrape(first, end):
   date = datetime.datetime(int(first[6:]), int(first[3:5]), int(first[:2]))
   last_date = datetime.datetime(int(end[6:]), int(end[3:5]), int(end[:2]))
   def get_day_matches(date):
      page = requests.get(f"https://www.yallakora.com/match-center?date={date}#days")
      src = page.content
      soup = BeautifulSoup(src, "lxml")
      championShips = soup.find_all('div', {'class':'matchCard'})
      match_details = []
      for championShip in championShips:
         title = championShip.find('div', {'class':'title'}).find('h2').text.strip()
         match_list = championShip.find_all('li')
         for match in match_list:
               teamA = match.find('div', {'class':'teamA'}).find('p').text.strip()
               teamB = match.find('div', {'class':'teamB'}).find('p').text.strip()
               match_nums = match.find('div', {'class':'MResult'})
               match_time = match_nums.find('span', {'class':'time'}).text.strip()
               match_result = f"{match_nums.find_all('span', {'class':'score'})[0].text.strip()} - {match_nums.find_all('span', {'class':'score'})[1].text.strip()}"
               match_details.append({
                  "نوع البطولة":title,
                  "الفريق الاول": teamA,
                  "الفريق الثاني": teamB,
                  "النتيجة": match_result if match_result != '- - -' else "لم بتدا المباراة بعد",
                  "الوقت": match_time,
                  "التاريخ":date.strftime('%x')
               })
      return match_details

   # writing the output into csv file
   keys = ['نوع البطولة', 'الفريق الاول', 'الفريق الثاني', 'النتيجة', 'الوقت', 'التاريخ']
   with open("matches.csv", 'w', newline='') as output_file:
      dict_writer = csv.DictWriter(output_file, keys)
      dict_writer.writeheader()
      while date != last_date:
         dict_writer.writerows(get_day_matches(date))
         Label(text =f"{date.strftime('%x')} day is created!".title()).pack()
         date += datetime.timedelta(days=1)
