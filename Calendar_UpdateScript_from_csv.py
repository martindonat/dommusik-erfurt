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
						
			time_str = row['Uhrzeit']
			if len(time_str) < 4: time_str += ".00"
			
			# Umwandlung von Datum und Uhrzeit in datetime-Objekte
			date_obj = dt.datetime.strptime(row['Datum'] + "/" + time_str, '%d.%m.%Y/%H.%M')
			
			# Erstellen des Dictionarys für eine Zeile
			row_dict = {
				'DatumZeit': date_obj,
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
unserer Chöre, Ensembles und Künstler im Dom oder in den katholischen Kirchen Erfurts.'
subsubtitle: '<p class="icon {{ solid fa-arrow-right }}"> Weitere Termine finden Sie <a href="kalender">hier.'
dates:
"""

yml_date = """  - icon: '{0}'
    title: '{1}'
    body: '<b>{2} Uhr {3}</b><br />{4}'
"""

calendar_overview_md_header = """+++
title = 'Kalender'
date = 2024-02-04T16:48:08+01:00
draft = false
image = '../images/Kalender_GR3.jpg'
+++

## Überblick über die kommenden Veranstaltungen
"""

calendar_overview_table_head = """| Datum | Uhrzeit | Ort | Beschreibung |
|-------|---------|-----|--------------|
"""

calendar_overview_md_footer = '\n\n{{<icon class="fa fa-arrow-left">}}&nbsp;[Zurück zu den aktuellen Terminen](../#three)'

##########################################################################
# Fixed Variables

log_file = 'Calendar_UpdateScript_Logs.log'
hugo_calendar_data_file = 'data/three.yml'
hugo_calendar_overview_file = 'content/kalender.md'
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
list_of_event_dicts.sort(key=lambda x: x['DatumZeit'])

# Remove past Events
for event in list_of_event_dicts:
	if event['DatumZeit'] < now:
		logging.info('Removing event "{0}" from {1}'.format(event["Text"], 
						event["DatumZeit"].strftime('%d. %B %Y')))
list_of_event_dicts = [ event for event in list_of_event_dicts if event['DatumZeit'] >= now ]

# Check if number of displayed events should be increased 
# When 6 events in next 4 weeks --> display 6 events instead of 4
if len(list_of_event_dicts) > 5:
	if (list_of_event_dicts[5]['DatumZeit'] - now < dt.timedelta(days=29)):
		logging.info('More than 5 events in the next 4 weeks, increasing number of displayed events...')
		number_of_displayed_events = 6


# Writing Calendar Overview
logging.info('Writing a overview file "{0}"...'.format(hugo_calendar_overview_file))
with open(hugo_calendar_overview_file, 'w') as f:
	
	f.write(calendar_overview_md_header)
	
	current_year = list_of_event_dicts[0]['DatumZeit'].year
	current_month = list_of_event_dicts[0]['DatumZeit'].strftime('%B')
	
	f.write("\n## {0}".format(current_year))

	f.write("\n\n### {0}".format(current_month))
	
	f.write("\n\n{0}".format(calendar_overview_table_head))
	
	for i in range(len(list_of_event_dicts)):

		if list_of_event_dicts[i]['DatumZeit'].year != current_year:
			# Jahreswechsel
		
			current_year = list_of_event_dicts[i]['DatumZeit'].year
			current_month = list_of_event_dicts[i]['DatumZeit'].strftime('%B')
			
			f.write("\n## {0}\n\n### {1}\n\n{2}".format(current_year, current_month, calendar_overview_table_head))
		
		elif list_of_event_dicts[i]['DatumZeit'].strftime('%B') != current_month:
			# Nur Monatswechsel ohne Jahreswechsel
		
			current_month = list_of_event_dicts[i]['DatumZeit'].strftime('%B')
			
			f.write("\n\n### {0}\n\n{1}".format(current_month, calendar_overview_table_head))
		
		
		# Write Event in table
		f.write("| {0} | {1} | {2} | {3} |\n".format(list_of_event_dicts[i]["DatumZeit"].strftime('%d. %B'),
						list_of_event_dicts[i]["DatumZeit"].strftime('%H.%M'),
						list_of_event_dicts[i]["Ort"],
						list_of_event_dicts[i]["Text"]))
						
	
	f.write(calendar_overview_md_footer)



logging.info('Overview file "{0}" written...'.format(hugo_calendar_overview_file))



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
						current_event["DatumZeit"].strftime('%d. %B %Y'),
						current_event["DatumZeit"].strftime('%H.%M'),
						current_event["Ort"],
						current_event["Text"]))
			

logging.info('END: calendar script ended succesfully')



