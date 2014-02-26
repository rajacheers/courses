# 6.00.1x Problem Set 7
# RSS Feed Filter

import feedparser
import string
import time
from project_util import translate_html
from Tkinter import *

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        summary = translate_html(entry.summary)
        try:
            subject = translate_html(entry.tags[0]['term'])
        except AttributeError:
            subject = ""
        newsStory = NewsStory(guid, title, subject, summary, link)
        ret.append(newsStory)
    return ret

#======================
# Part 1
# Data structure design
#======================

class NewsStory:
    def __init__(self,guid,title,subject,summary,link):
        self.guid = guid
        self.title = title
        self.subject = subject
        self.summary = summary
        self.link = link
    def getGuid(self):
        return self.guid
    def getTitle(self):
        return self.title
    def getSubject(self):
        return self.subject
    def getSummary(self):
        return self.summary
    def getLink(self):
        return self.link

#======================
# Part 2
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        raise NotImplementedError

import string
class WordTrigger(Trigger):
    def __init__(self, word):
        self.word = word.lower()
    def isWordIn(self,text):
        text = text.lower()
        for a in string.punctuation:
            text = text.replace(a,' ') 
        words = text.split(' ')
        if self.word in words:
            return True
        return False

class TitleTrigger(WordTrigger):
    def evaluate(self, text):    
        return self.isWordIn(text.getTitle())

class SubjectTrigger(WordTrigger):
    def evaluate(self, text):    
        return self.isWordIn(text.getSubject())

class SummaryTrigger(WordTrigger):
    def evaluate(self, text):    
        return self.isWordIn(text.getSummary())

class NotTrigger(Trigger):
    def __init__(self,Trigger):
        self.T=Trigger  
    def evaluate(self, x):
        return not self.T.evaluate(x)

class AndTrigger(Trigger):
    def __init__(self,T1,T2):
        self.T1=T1
        self.T2=T2
    def evaluate(self, x):
        return self.T1.evaluate(x) and self.T2.evaluate(x)

class OrTrigger(Trigger):
    def __init__(self,T1,T2):
        self.T1=T1
        self.T2=T2  
    def evaluate(self, x):
        return self.T1.evaluate(x) or self.T2.evaluate(x)

class PhraseTrigger(Trigger):
    def __init__(self, phrase):
        self.phrase = phrase
    def evaluate(self, text):
        if self.phrase in (text.getTitle() + text.getSubject() + text.getSummary()):
            return True
        return False


#======================
# Part 3
# Filtering
#======================

def filterStories(stories, triggerList):
    a=[]
    for story in stories:
        for trigger in triggerList:
	    if trigger.evaluate(story) and story not in a:
		print story
                a=a.append(story)
    #return a
    return stories

#======================
# Part 4
# User-Specified Triggers
#======================

def makeTrigger(triggerMap, triggerType, params, name):
    if triggerType == 'TITLE':
        trig = TitleTrigger(params[0])
        triggerMap[name] = trig
    elif triggerType == 'SUBJECT':
        trig = SubjectTrigger(params[0])
        triggerMap[name] = trig
    elif triggerType == 'SUMMARY':
        trig = SummaryTrigger(params[0])
        triggerMap[name] = trig
    elif triggerType == 'NOT':
        trig = NotTrigger(triggerMap[params[0]])
        triggerMap[name] = trig
    elif triggerType == 'AND':
        trig = AndTrigger(triggerMap[params[0]],triggerMap[params[1]])
        triggerMap[name] = trig
    elif triggerType == 'OR':
        trig = OrTrigger(triggerMap[params[0]],triggerMap[params[1]])
        triggerMap[name] = trig
    elif triggerType == 'PHRASE':
        trig = PhraseTrigger(' '.join(params[:]))
        triggerMap[name] = trig
    return trig


def readTriggerConfig(filename):
    """
    Returns a list of trigger objects
    that correspond to the rules set
    in the file filename
    """

    triggerfile = open(filename, "r")
    all = [ line.rstrip() for line in triggerfile.readlines() ]
    lines = []
    for line in all:
        if len(line) == 0 or line[0] == '#':
            continue
        lines.append(line)

    triggers = []
    triggerMap = {}

    for line in lines:

        linesplit = line.split(" ")

        # Making a new trigger
        if linesplit[0] != "ADD":
            trigger = makeTrigger(triggerMap, linesplit[1],
                                  linesplit[2:], linesplit[0])

        # Add the triggers to the list
        else:
            for name in linesplit[1:]:
                triggers.append(triggerMap[name])

    return triggers
    
import thread

SLEEPTIME = 60 #seconds -- how often we poll


def main_thread(master):
    # A sample trigger list - you'll replace
    # this with something more configurable in Problem 11
    try:
        # These will probably generate a few hits...
        t1 = TitleTrigger("Obama")
        t2 = SubjectTrigger("Romney")
        t3 = PhraseTrigger("Election")
        t4 = OrTrigger(t2, t3)
        triggerlist = [t1, t4]
        
        triggerlist = readTriggerConfig("triggers.txt")

        # **** from here down is about drawing ****
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)
        
        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)

        # Gather stories
        guidShown = []
        def get_cont(newstory):
            if newstory.getGuid() not in guidShown:
                cont.insert(END, newstory.getTitle()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.getSummary())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.getGuid())

        while True:

            print "Polling . . .",
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://rss.news.yahoo.com/rss/topstories"))

            # Process the stories
            stories = filterStories(stories, triggerlist)

            map(get_cont, stories)
            scrollbar.config(command=cont.yview)


            print "Sleeping..."
            time.sleep(SLEEPTIME)

    except Exception as e:
        print e


if __name__ == '__main__':

    root = Tk()
    root.title("Some RSS parser")
    thread.start_new_thread(main_thread, (root,))
    root.mainloop()

