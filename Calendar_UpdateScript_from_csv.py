## Description

# Import Modules
import datetime as dt
import logging
import csv
import locale
import sys


##########################################################################
# Functions


def check_description_for_keywords(description, keywords_list):
	'''Function takes a string and a keyword list
	and returns whether one of the keywords can be found in the string'''
	return_value = False
	
	for word in keywords_list:
		if word in description:
			return_value = True
			break
	
	return return_value
		


def process_csv_file_to_list(file_path):
	'''Function takes a file path (to the csv to be processed)
	and returns a list of dictionaries containing the information'''
	
	data = []
	
	with open(file_path, newline='') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			# Umwandlung von Datum und Uhrzeit in datetime-Objekte
			date_obj = dt.datetime.strptime(row['Datum'], '%d.%m.%Y')
			#time_obj = dt.datetime.strptime(row['Uhrzeit'], '%H:%M:%S').time()
			
			# Erstellen des Dictionarys für eine Zeile
			row_dict = {
				'Datum': date_obj,
				'Uhrzeit': row['Uhrzeit'],
				'Ort': row['Ort'],
				'Text': row['Text']
			}
			# Hinzufügen des Dictionarys zur Liste von Daten
			data.append(row_dict)
	return data


def auto_select_icon(description_str):
	keywords_mass = ['Messe', 'Hochamt']
	keywords_organ = ['Orgel']
	keywords_choir = ['Chor', 'Ensemble']
	
	if check_description_for_keywords(description_str, keywords_mass):
		icon_str = 'solid fa-church'
	
	elif check_description_for_keywords(description_str, keywords_choir):
		icon_str = 'solid fa-users'
	
	else:
		icon_str = 'solid fa-music'
		
	return icon_str



##########################################################################
# File Strings

yml_header = """---
enable: true
title: 'Aktuelle Termine'
"""

yml_subtitle_zero_events = """subtitle: 'Nachfolgend finden Sie aktuelle liturgische Auftritte oder außerliturgische Konzerte
unserer Chöre, Ensembles und Künstler im Dom oder in den katholischen Kirchen Erfurts.
<br/><br/><br/><br/>
<i>– Aktuell liegen keine Termine vor. –</i>'
"""

yml_subtitle_events = """subtitle: 'Nachfolgend finden Sie aktuelle liturgische Auftritte oder außerliturgische Konzerte
unserer Chöre, Ensembles und Künstler im Dom oder in den katholischen Kirchen Erfurts.
<br/><br/>Weitere Details zu den Konzerten im Dom finden Sie <a href="https://dom-erfurt.de/index.php?article_id=19">hier</a>.'
dates:
"""

yml_date = """  - icon: '{0}'
    title: '{1}'
    body: '<b>{2} Uhr {3}</b><br />{4}'
"""


##########################################################################
# Fixed Variables

log_file = 'Calendar_UpdateScript_Logs.log'
hugo_calendar_data_file = 'data/three.yml'
calendar_csv = 'Kalender_Termine.csv'
number_of_displayed_events = 4

locale.setlocale(locale.LC_ALL, "de_DE.UTF8")

##########################################################################
# Begin of script

logging.basicConfig(filename=log_file, format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
logging.info('START: starting calendar script...')

today = dt.date.today()
now = dt.datetime.now()

# Import Events
logging.info('Importing events from {0}...'.format(calendar_csv))
list_of_MusicEvents = []

# Get a list of dictionaries with the events
try:
	list_of_event_dicts = process_csv_file_to_list(calendar_csv)
except FileNotFoundError:
	logging.error('Could not find CSV file. Aborting the process.')
	sys.exit()

# Sort Events by date
list_of_event_dicts.sort(key=lambda x: x['Datum'])

# Remove past Events
for event in list_of_event_dicts:
	if event['Datum'] < now:
		logging.info('Removing event "{0}" from {1}'.format(event["Text"], 
						event["Datum"].strftime('%d. %B %Y')))
list_of_event_dicts = [ event for event in list_of_event_dicts if event['Datum'] >= now ]

# Check if number of displayed events should be increased 
# When 6 events in next 4 weeks --> display 6 events instead of 4
if len(list_of_event_dicts) > 5:
	if (list_of_event_dicts[5]['Datum'] - now < dt.timedelta(days=29)):
		logging.info('More than 5 events in the next 4 weeks, increasing number of displayed events...')
		number_of_displayed_events = 6

# Shorten List to displayed events
if len(list_of_event_dicts) > number_of_displayed_events:
	del list_of_event_dicts[number_of_displayed_events:]


# Determine definite number of displayed events
number_of_displayed_events = min(number_of_displayed_events, len(list_of_event_dicts))

logging.info('Number of displayed events will be: {0}'.format(number_of_displayed_events))



# WRITING
logging.info('Writing a new file "{0}"...'.format(hugo_calendar_data_file))
with open(hugo_calendar_data_file, 'w') as f:
	
	f.write(yml_header)
	
	if number_of_displayed_events == 0:
		
		logging.warning('No events available')
		f.write(yml_subtitle_zero_events)
		
	else:
	
		f.write(yml_subtitle_events)
		
		for i in range(number_of_displayed_events):
			
			current_event = list_of_event_dicts[i]
			
			icon_str = auto_select_icon(current_event["Text"])
			
			f.write(yml_date.format(icon_str,
						current_event["Datum"].strftime('%d. %B %Y'),
						current_event["Uhrzeit"],
						current_event["Ort"],
						current_event["Text"]))
			

logging.info('END: calendar script ended succesfully')



