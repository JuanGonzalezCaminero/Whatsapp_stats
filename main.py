import sys
import re
import collections
import heapq
from operator import itemgetter
import datetime
import numpy as np
import calendar
from calendar import monthrange
import matplotlib.pyplot as plt

text_characters=list("abcdefghijklmnñopqrstuvwxyzáéíóúñ ")

def messages_reader(file):
	message_regex = re.compile(r"^[0-9]{2}/[0-9]{2}/[0-9]{4}, [0-9]{2}:[0-9]{2} - [a-zA-Záéíóúñ0-9+ ]*: .*")
	date_regex = re.compile(r"^[0-9]{2}/[0-9]{2}/[0-9]{4}")
	time_regex = re.compile(r"^[0-9]{2}:[0-9]{2}")
	user_regex = re.compile(r"[a-zA-Záéíóúñ0-9+ ]*")
	link_regex = re.compile(r"http[s]?://[^ ]*")

	#Get the first message that isn't information/status
	while True:
		message=file.readline()
		if message_regex.match(message):
			break

	for line in file:
		#If the line is the start of the next message
		if date_regex.search(line):
			if not message_regex.match(line):
				#Not a message (information or others) ignore it
				continue
			#Extract the fields from the current message and return them,
			#store the start of the next message
			date_match=date_regex.search(message)
			date=date_match.group()
			message=message[12:]
			time_match=time_regex.search(message)
			time=time_match.group()
			message=message[8:]
			user_match=user_regex.search(message)
			user=user_match.group()
			text=message[len(user)+1:].lower()

			#remove links
			text=link_regex.sub("", text)

			#Include spaces for instances with special characters preceded and followed 
			#by words with no spaces in between
			text=''.join([i if i in text_characters else " " for i in text ])
			
			#substitute all sequences of multiple spaces with one space
			text=re.sub(r" +", " ", text).strip()

			message=line
			yield date, time, user, text
		else:
			message = message.rstrip("\n")
			#for some cases where a space is not present before the new line
			message = message+" "
			message+=line

	#All this hassle for the last message:
	date_match=date_regex.search(message)
	date=date_match.group()
	message=message[12:]
	time_match=time_regex.search(message)
	time=time_match.group()
	message=message[8:]
	user_match=user_regex.search(message)
	user=user_match.group()
	text=message[len(user)+1:].lower()
	text=link_regex.sub("", text)
	text=''.join([i if i in text_characters else " " for i in text ])
	text=re.sub(r" +", " ", text).strip()

	yield date, time, user, text


if len(sys.argv) < 2:
	print("Usage: python3 main.py <filename>")

file=open(sys.argv[1])

#Data structures used for counting
#"user":defaultdict(int)
word_counters={}
#defaultdict(int)
message_counter=collections.defaultdict(int)
#defaultdict "user":list of datetimes
message_datetimes=collections.defaultdict(list)
#dict year:list of 12 months (each month is a list of days))
#Cant make it a defaultdict because there is no way to pass
#the year to the factory, wich in turn makes it impossible 
#to generate the correct number of days. An alternative would 
#be to always generate the same year and add an extra day to 
#february if needed manually
date_counters={}

for date, time, user, text in messages_reader(file):
	#Transform the date and time into a datetime object
	date_time = datetime.datetime.strptime(date+" "+time, "%d/%m/%Y %H:%M")

	#If it's the first time this user appears, add a 
	#word counter
	if user not in word_counters:
		word_counters[user] = collections.defaultdict(int)
	
	#Add to total messages by the user
	message_counter[user]+=1
	#Add the datetime to the user's list
	message_datetimes[user].append(date_time)

	if(text==""):
		#No text due to the message being only emojis or 
		#special characters, the message is counted but 
		#the words are not processed (it would only add '' 
		#to the dictionary)
		continue

	for word in text.split(" "):
		word_counters[user][word] += 1

for user in word_counters:
	print(user)
	unique_words=0
	total_words=0
	for word in word_counters[user]:
		unique_words += 1
		total_words += word_counters[user][word]
	print(str(message_counter[user]) + " messages")
	print(str(total_words) + " total words")
	print(str(unique_words) + " unique words")
	#top 10 most used words
	most_used = heapq.nlargest(10, word_counters[user].items(), key=itemgetter(1))
	print(most_used)
	#print(word_counters[user])
	#breakpoint()

	#Accumulate date values
	user_datetimes=message_datetimes[user]
	years = np.unique([dt.year for dt in user_datetimes])
	for year in years:
		date_counters[year]=[]
		for month in range(1,13):
			date_counters[year].append([])
			for day in range(monthrange(year, month)[1]):
				date_counters[year][-1].append(0)
	for date in user_datetimes:
		#print(str(date.year) + " " + str(date.month-1) + " " + str(date.day) + " ")
		#print(len(date_counters[date.year][date.month-1]))
		date_counters[date.year][date.month-1][date.day-1]+=1

	for year in years:
		print("Year: " + str(year))
		print("Total messages: " + str(np.sum([np.sum(month) for month in date_counters[year]])))
		for month in range(1,13):
			print(calendar.month_name[month])
			print(str(np.sum(date_counters[year][month-1])) + " messages")

	#Bar chart with messages per month
	fig, ax = plt.subplots()
	for year in years:
		ax.bar(list(calendar.month_abbr)[1:], [np.sum(date_counters[year][month]) for month in range(12)])
	plt.show()








