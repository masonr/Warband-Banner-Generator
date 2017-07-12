#!/usr/bin/python
import os;
import sys;
import bleach;

import cgi;
import cgitb;
cgitb.enable();

import urllib2;
import xml.etree.ElementTree as ET;

from PIL import Image;
from PIL import ImageFont;
from PIL import ImageDraw;

print("Content-Type: image/png\r\n");

banners = {
	'cannons': 'cannons.png',
	'civilwar_scene': 'civil_war_scene.png',
	'civilwar_scene2': 'picketts_charge.png',
	'nw_borodino': 'borodino.png',
	'nw_scene': 'nw_french.png',
	'mnb_cavalry': 'cavalry.png',
	'mnb_mounted': 'mounted.png'
};
images_directory = "./images/";

arguments = cgi.FieldStorage();
ip = bleach.clean(arguments["ip"].value);
port = bleach.clean(arguments["port"].value);

banner = banners[bleach.clean(arguments["banner"].value)];

img = Image.open(os.path.join(images_directory, banner)).convert('RGBA');
draw = ImageDraw.Draw(img);
font1 = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', 14);
font2 = ImageFont.truetype('Pillow/Tests/fonts/DejaVuSans.ttf', 18);

link = "http://" + ip + ":" + port;
try: 
	f = urllib2.urlopen(link, None, 5);
except:
	error = 'Error Retrieving Server Details';
	w, h = draw.textsize(error, font2);
	draw.text((249-(w/2),1),error,(0,0,0),font=font2);
	draw.text((251-(w/2),1),error,(0,0,0),font=font2);
	draw.text((249-(w/2),3),error,(0,0,0),font=font2);
	draw.text((251-(w/2),3),error,(0,0,0),font=font2);
	draw.text((250-(w/2),2),error,(255,0,0),font=font2);		
	img.save('banner-mod.png', 'png');
	print(file('banner-mod.png', 'rb').read());
	os.remove('banner-mod.png');
	sys.exit(0);

stats = f.read();

e = ET.fromstring(stats);
serverName = bleach.clean(e.getiterator(tag='Name')[0].text);
module = bleach.clean(e.getiterator(tag='ModuleName')[0].text);
type = bleach.clean(e.getiterator(tag='MapTypeName')[0].text);
map = bleach.clean(e.getiterator(tag='MapName')[0].text);
players = bleach.clean(e.getiterator(tag='NumberOfActivePlayers')[0].text) + " / " + bleach.clean(e.getiterator(tag='MaxNumberOfPlayers')[0].text);
status = bleach.clean(e.getiterator(tag='HasPassword')[0].text);

if status == 'No':
	lock = Image.open(os.path.join(images_directory, 'unlocked.png')).convert('RGBA');
else:
	lock = Image.open(os.path.join(images_directory, 'locked.png')).convert('RGBA');

# Draw Header
game = 'Mount & Blade: Warband'
w, h = draw.textsize(game, font2);
draw.text((249-(w/2),1),game,(0,0,0),font=font2);
draw.text((251-(w/2),1),game,(0,0,0),font=font2);
draw.text((249-(w/2),3),game,(0,0,0),font=font2);
draw.text((251-(w/2),3),game,(0,0,0),font=font2);
draw.text((250-(w/2),2),game,(255,255,255),font=font2);

# Draw Eval Server
draw.text((8, 28),'Server Name:',(0,0,0),font=font1);
draw.text((9, 40),serverName,(0,0,0),font=font2);
draw.text((11, 40),serverName,(0,0,0),font=font2);
draw.text((9, 42),serverName,(0,0,0),font=font2);
draw.text((11, 42),serverName,(0,0,0),font=font2);
draw.text((10, 41),serverName,(255,255,255),font=font2);

# Draw Eval Module
draw.text((8, 66),'Module:',(0,0,0),font=font1);
draw.text((9, 78),module,(0,0,0),font=font2);
draw.text((11, 78),module,(0,0,0),font=font2);
draw.text((9, 80),module,(0,0,0),font=font2);
draw.text((11, 80),module,(0,0,0),font=font2);
draw.text((10, 79),module,(255,255,255),font=font2);

# Draw Game Type
draw.text((8, 104),'Game Mode:',(0,0,0),font=font1);
draw.text((9, 116),type,(0,0,0),font=font2);
draw.text((11,116),type,(0,0,0),font=font2);
draw.text((9,118),type,(0,0,0),font=font2);
draw.text((11,118),type,(0,0,0),font=font2);
draw.text((10,117),type,(255,255,255),font=font2);

# Draw Current Map
w, h = draw.textsize('Current Map:', font1);
draw.text((492-w, 28),'Current Map:',(0,0,0),font=font1);
w, h = draw.textsize(map, font2);
draw.text((489-w, 40),map,(0,0,0),font=font2);
draw.text((491-w, 40),map,(0,0,0),font=font2);
draw.text((489-w, 42),map,(0,0,0),font=font2);
draw.text((491-w, 42),map,(0,0,0),font=font2);
draw.text((490-w, 41),map,(255,255,255),font=font2);

# Draw Number of Players
w, h = draw.textsize('Current Players:', font1);
draw.text((492-w, 66),'Current Players:',(0,0,0),font=font1);
w, h = draw.textsize(players, font2);
draw.text((489-w, 78),players,(0,0,0),font=font2);
draw.text((491-w, 78),players,(0,0,0),font=font2);
draw.text((489-w, 80),players,(0,0,0),font=font2);
draw.text((491-w, 80),players,(0,0,0),font=font2);
draw.text((490-w, 79),players,(255,255,255),font=font2);

# Draw Lock/Unlocked Symbol
img.paste(lock, (474,4));

img.save('banner-mod.png', 'png');
print(file('banner-mod.png', 'rb').read());
os.remove('banner-mod.png');
