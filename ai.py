import pyttsx3
import speech_recognition
import time
import sys
import ctypes
import wikipedia
import datetime
import json
import re
import webbrowser
import smtplib
import requests
import urllib
import os
import urllib.request as urllib2
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from time import strftime
from youtube_search import YoutubeSearch

path = 'E:\chromedriver\chromedriver.exe'

def speak(text):
	print("Bot: {}".format(text))
	m = pyttsx3.init()
	m.say(text)
	m.runAndWait()

def get_audio():
	r = speech_recognition.Recognizer()
	with speech_recognition.Microphone() as mic:
		print("Me: ", end='')
		audio = r.listen(mic, phrase_time_limit=5)
		try:
			text = r.recognize_google(audio)
			print(text)
			return(text)
		except:
			print("...")
			return 0
def stop():
	speak("See you again!")
def get_text():
	for i in range(3):
		text = get_audio()
		if text:
			return text.lower()
		elif i < 2:
			speak("Sorry I can't hear you! Can you repeat it again?")
	time.sleep(2)
	stop()
	return 0

def hello(name):
	day_time = int(strftime('%H'))
	if day_time < 12:
		speak("Good morning {}! Have a nice day.".format(name))
	elif 12 <= day_time < 18:
		speak("Good afternoon {}! What's are you gonna do?".format(name))
	else:
		speak("Good night {}! How is your day?".format(name))

def get_time(text):
	now = datetime.datetime.now()
	if "hour" in text or "time" in text or "now" in text:
		speak("It's %d o'clock %d" % (now.hour, now.minute))
	elif "day" in text or "date" in text:
		speak("Today is %d of %d, %d" % (now.day, now.month, now.year))
	else:
		speak("Sorry I can't hear you! Can you repeat it again?")

def open_application(text):
	if "Google" in text or "Chrome" in text:
		speak("Opening Google Chrome")
		os.startfile('C:\Program Files (x86)\Google\Chrome\Application\chrome.exe')
	elif "Word" in text:
		speak("Opening Microsoft Word")
		os.startfile('C:\Program Files\Microsoft Office\Office16\WINWORD.EXE')
	elif "Excel" in text:
		speak("Opening Microsoft Excel")
		os.startfile('C:\Program Files\Microsoft Office\Office16\EXCEL.EXE')
	else:
		speak("Your requested application hasn't been installed yet!")
def open_website(text):
	reg_ex = re.search('open (.+)', text)
	if reg_ex:
		domain = reg_ex.group(1)
		url = 'https://www.' + domain
		webbrowser.open(url)
		speak("Your requested website is opened!")
		return True
	else:
		return False

def send_email(text):
	speak("Who do you want to send email for")
	recipient = get_text()
	if "friend" in recipient:
		speak("What do you want to send?")
		content = get_text()
		mail = smtplib.SMTP('smtp.gmail.com', 587)
		mail.ehlo()
		mail.starttls()
		mail.login('tranlamxyz610@gmail.com', 'ABC123456789@')
		mail.sendmail('tranlamxyz610@gmail.com',
					  'lamxyz610@gmail.com', content.encode('utf-8'))
		mail.close()
		speak("Your email is sent!")
	else:
		speak("Sorry I can't find the requested oponents in your list?")

def current_weather():
	speak("Which city are you looking for?")
	ow_url = "http://api.openweathermap.org/data/2.5/weather?"
	city = get_text()
	if not city:
		pass
	api_key = "fe8d8c65cf345889139d8e545f57819a"
	call_url = ow_url + "appid=" + api_key + "&q=" + city + "&units=metric"
	response = requests.get(call_url)
	data = response.json()
	if data["cod"] != "404":
		city_res = data["main"]
		current_temperature = city_res["temp"]
		current_pressure = city_res["pressure"]
		current_humidity = city_res["humidity"]
		suntime = data["sys"]
		sunrise = datetime.datetime.fromtimestamp(suntime["sunrise"])
		sunset = datetime.datetime.fromtimestamp(suntime["sunset"])
		wthr = data["weather"]
		weather_description = wthr[0]["description"]
		now = datetime.datetime.now()
		content = """
		Today is date {day} of {month}, {year}
		Sun rises at {hourrise} o'clock {minrise}
		Sun sets at {hourset} o'clock {minset}
		The avarage temperature is {temp} C degree
		Air pressure is {pressure} Pascal
		Humidity is {humidity}%.""".format(day = now.day,month = now.month, year= now.year, hourrise = sunrise.hour, minrise = sunrise.minute,
																		   hourset = sunset.hour, minset = sunset.minute, 
																		   temp = current_temperature, pressure = current_pressure, humidity = current_humidity)
		speak(content)
		time.sleep(20)
	else:
		speak("Sorry I can't find your requested city")

def play_song():
	speak("Please pick a song!")
	time.sleep(3)
	mysong = get_text()
	while True:
		result = YoutubeSearch(mysong, max_results=10).to_dict()
		if result:
			break
	url = 'https://www.youtube.com' + result[1]['url_suffix']
	webbrowser.open(url)
	speak("The requested song is opened!")

def read_news():
	speak("What do you want to read about?")
	
	queue = get_text()
	params = {
		'apiKey': '30d02d187f7140faacf9ccd27a1441ad',
		    "q": queue,
	}
	api_result = requests.get('http://newsapi.org/v2/top-headlines?', params)
	api_response = api_result.json()
	print("News")
	
	for number, result in enumerate(api_response['articles'], start=1):
		print(f"""News {number}:\nTitle: {result['title']}\nDescription: {result['description']}\nLink: {result['url']}
	""")
	if number <= 3:
		webbrowser.open(result['url'])

def tell_me_about():
	try:
		speak("What are you looking for?")
		text = get_text()
		contents = wikipedia.summary(text).split('\n')
		speak(contents[0])
		time.sleep(10)
		for content in contents[1:]:
			speak("Is there anything you want to know?")
			ans = get_text()
			if "yes" not in ans:
				break
			speak(content)
			time.sleep(10)
	
		speak("Thank you for listening!")
	except:
		speak("Sorry I can't understand. Please repeat again!")

def help_me(name):
	speak("""I can help {} with:
	1. Greeting
	2. Checking current date, time
	3. Opening website, application
	4. Sending email
	5. Weather forecast
	6. Opening music video
	7. Reading today news
	8. Searching wikipedia """)

def assisstant():
	speak("Hello sir, What's your name?")
	name = get_text()
	if name == "":
		speak("Sorry I can't hear you! Can you repeat it again?")
		name = get_text()
	else:
		speak("Hello {}".format(name))
		speak("How can i help you?")
		while True:
			text = get_text()
			if not text:
				break
			elif "break" in text or "stop" in text or "bye" in text:
				stop()
				break
			elif "can you do" in text:
				help_me(name)
			elif "hello" in text or "hi" in text or "good" in text:
				hello(name)
			elif "now" in text or "time" in text or "date" in text:
				get_time(text)
			elif "open" in text:
				if "." in text:
					open_website(text)
				else:
					open_application(text)
			elif "email" in text or "mail" in text or "gmail" in text:
				send_email(text)
			elif "weather" in text or "temperature" in text or "humidity" in text:
				current_weather()
			elif "song" in text or "youtube" in text:
				play_song()
			elif "news" in text:
				read_news()
			elif "meaning" in text or "searching" in text or "wikipedia" in text:
				tell_me_about()
			else:
				speak("How can i help you?")

assisstant()