from datetime import datetime
from html import escape
from rfeed import Guid, Item, Feed
from requests import Session
from .extensions import WebfeedsIcon, Webfeeds
from json import loads

session = Session()

URL = "https://cse.google.com/cse/element/v1"
QUERY = {
	"num": 20,
	"cx": "007638134514443209427:kjalhbutdxc",
	"q": None,
	"safe": "off",
	"cse_tok": "AJvRUv3U3y44RFcweP48CvpDkB5P:1633792129891",
	"sort": "date",
	"callback": "google.search.cse.api18483"
}

IMG_TEMPLATE = "<img src='{}'>"

def generate_item(result: dict):
	thumbnail = result.get("richSnippet", {}).get("cseThumbnail", {}).get("src")
	content = result.get("content", "")

	description = IMG_TEMPLATE.format(escape(thumbnail, quote=True)) + content if thumbnail else content

	title = result.get("title")
	link = result.get("url")

	# Might be able to add published times if I make calls to an API
	# or someone makes a timeago parser.
	info = {
		"title": title,
		"link": link,
		"guid": Guid(link),
		"author": "Anonymous",
		"description": description
	}

	return Item(**info)


def create_feed():
	res = session.get(URL, params={**QUERY, "q": "source code leak"})
	text = res.text

	startidx = text.find('(')
	endidx = text.rfind(')')
	body = loads(text[startidx + 1 : endidx])
	
	icon = WebfeedsIcon("https://s.4cdn.org/image/apple-touch-icon-ipad-retina.png")

	DESCRIPTION = "Too much cool stuff leaks on that godawful website, so let's visit it as little as possible."

	info = {
		"title": "4chan Leaks",
		"description": DESCRIPTION,
		"link": "https://4chan.org",
		"items": map(generate_item, body["results"]),
		"extensions": [
			Webfeeds(),
			icon,
		],
		"lastBuildDate": datetime.now(),
	}

	return Feed(**info)
