from urllib.request import urlopen
from urllib.error import (
	HTTPError,
	URLError
)
from bs4 import BeautifulSoup
import csv
import re
import dryscrape

def fill_csv_info(info):
	length = len(info["dates"])
	try:
		with open("results.csv", "w") as csvfile:
			filewriter = csv.writer(csvfile, delimiter=',')
			filewriter.writerow(["Date", "Title", "Content"])
			for i in range(0, length):
				filewriter.writerow([info["dates"][i], info["titles"][i], info["content"][i]])
	except:
		print("Error during csv file writing")

def	get_urls(bs):
	urls = []
	for url in bs:
		urls.append(url.attrs['href'])
	return (urls)

def get_titles(bs):
	result = []
	titles = bs.find('div', {'id':'dle-content'}).find_all('a')
	if titles == None:
		print ("Attribute is not found")
		exit(1)
	else:
		for title in titles:
			result.append(title.get_text())
		return (result, titles)

def get_dates(bs):
	all_date = []
	try:
		dates = bs.find_all('span', {'class': re.compile('[.]*date[.]*')})
	except:
		print("No date was found")
		exit(1)
	length = len(dates)
	for i in range(1, length):
		all_date.append("{} {}".format(dates[0].get_text(), dates[i].get_text()))
	return (all_date)

def get_html_of_page(zakon_url):
	try:
		html = urlopen(zakon_url)
	except HTTPError as e:
		print(e)
	except URLError as e:
		print("Unknown URL")
	else:
		bs = BeautifulSoup(html.read(), 'html.parser')
		return (bs)

def get_contents(zakon_url, urls):
	result = []
	
	for url in urls:
		description = ""
		i = 0
		content = get_html_of_page(zakon_url + url)
		if (content == None):
			print("Couldn't get any content for url ({})".format(url))
			result.append(None)
		else:
			p_tags = content.find_all('p')
			for p_tag in p_tags:
				description += p_tag.get_text() + "\n"
			result.append(description)
	return (result)

def get_comments(zakon_url, urls):
	comments = []
	session = dryscrape.Session()
	for url in urls:
		session.visit(zakon_url + url)
		response = session.body()
		soup = BeautifulSoup(response, features="lxml")
		comments.append(soup.find(id="zkn_comments"))
	return (comments)

if __name__ == '__main__':
	zakon_url = "https://www.zakon.kz/news"
	bs = get_html_of_page(zakon_url)
	titles, tags = get_titles(bs)
	urls = get_urls(tags)
	date = get_dates(bs)
	content = get_contents(zakon_url, urls)
	comments = get_comments(zakon_url, urls)
	info = {}
	info["dates"] = date
	info["titles"] = titles
	info["content"] = content
	fill_csv_info(info)
