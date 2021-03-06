import os
import sys
import pickle
import urllib2
import subprocess
from datetime import datetime, date, timedelta

import string_utils

os.chdir(sys.path[0])

def get_magnet_link_from_pirate_bay(search_string, _cat='TV HD'):
    catagory = {'TV HD':'208', 'MOVIES HD':'207' }[_cat]
    search_url = "http://thepiratebay.se/search/%s/0/7/%s" % (search_string.replace(' ', '%20'), catagory)
    response = urllib2.urlopen(search_url)
    page_source = response.read()

    start_index = page_source.find('"magnet:')
    end_index = page_source.find('"', start_index+10)

    magnet_url_first_result = page_source[start_index+1:end_index]
    if not magnet_url_first_result.startswith('magnet:'):
        raise BaseException("Didn't get proper magnet url. Search url: %s, magnet_url: %s" % (search_url, magnet_url_first_result))
    return magnet_url_first_result

def add_to_client(magnet_url, binary="transmission-gtk"):
    print 'Adding: %s to client %s' % (magnet_url, binary)
    subprocess.call([binary, magnet_url])

class Episode(object):
    def __init__(self, number_in_series, season, number_in_season, title, original_air_date):
        self.season = season
        self.number_in_series = number_in_series
        self.number_in_season = number_in_season
        self.title = title
        self.original_air_date = original_air_date
        self.SiEj = 'S%sE%s' % (season.zfill(2), number_in_season.zfill(2))

    def is_in_future(self):
        return datetime.combine(self.original_air_date, datetime.min.time()) >  datetime.now()

    def is_downloadable(self, days_delta_to_be_considered_downloadable=1):
        return datetime.combine(self.original_air_date, datetime.min.time()) + timedelta(days=days_delta_to_be_considered_downloadable) <  datetime.now()

    def __str__(self):
        return '%s (%s in series), title: %s, original air date: %s%s' %\
                (self.SiEj, self.number_in_series, self.title, self.original_air_date, ' (future episode)' if self.is_in_future() else '')

class Show(object):
    '''
    This class is a huge mess...
    Shouldn't have anything to do with accessing wiki, the parsing is all shitty and wrong and the code is generally crap...
    But I was sick and bored when I wrote it, so I that's my excuse. One day I hope to tidy it up, but for now it works.
    Terrilbe design though.
    '''
    def __init__(self, name, last_seen_ep = None):
        self.name = name
        self.episodes = []
        self.last_seen_ep = last_seen_ep

    def add_episode(self, number_in_series, season, number_in_season, title, original_air_date):
        self.episodes.append(Episode(number_in_series, season, number_in_season, title.strip('"'), original_air_date))

    def get_wiki_list_of_episodes_page(self):
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        url = "http://en.wikipedia.org/wiki/List_of_%s_episodes" % (string_utils.camelcase(self.name, exceptions=['of', 'a', 'and']).replace(' ', '_'))
        print 'getting: ' + url
        infile = opener.open(url)
        page = infile.read()
        return page

    def parse_episodes_list_from_wikipedia(self):
        page = self.get_wiki_list_of_episodes_page()

        season = 0
        total_episodes = 0
        episodes_for_this_season = 100
        title = directed_by = written_by = original_air_date = None
        expect_td_tag_close = expect_main_article = expect_number_in_season = expect_title = expect_directed_by = expect_written_by = expect_original_air_date = False
        for line_number, line in enumerate(page.splitlines()):
            if expect_td_tag_close:
                if line.find('</td>') != -1:
                    expect_td_tag_close = False
                continue

            # For when we finish the episode list and (season hasn't started yet)
            if expect_main_article:
                if line.find('Main article') == -1 and line.find('table class=') == -1:
                    print "leaving because couldn't find main article at line: %s"  % (line_number)
                    return
                expect_main_article = False
                continue

            found_new_season = line.find('id="Season_')
            if found_new_season != -1:
                season = line[found_new_season+11:line.find('_', found_new_season+12)]
                expect_main_article = True
                print 'new season: %s' % (season)

            found_new_episode = line.find('id="ep')
            if found_new_episode != -1 and season > 0: # need to make sure we got to the season
                total_episodes = line[found_new_episode + 6 : line.find('"', found_new_episode+6)]
                expect_number_in_season = True
            elif expect_number_in_season:
                episodes_for_this_season = line[4:line.find('</', 5)]
                expect_number_in_season = False
                expect_title = True
            elif expect_title:
                # case type: <td class="summary" style="text-align: left;">"<a href="/wiki/Easy_Com-mercial,_Easy_Go-mercial" title="Easy Com-mercial, Easy Go-mercial">Easy Com-mercial, Easy Go-mercial</a>"</td>
                title_start_index = line.find('title="')
                if title_start_index != -1:
                    title = line[title_start_index + 7 :line.find('"', title_start_index + 8)]
                else:
                    title_start_index = line.find('style="text-align: left;">')
                    # case type: <td class="summary" style="text-align: left;">"Mazel-Tina"</td>
                    if title_start_index != -1:
                        title = line[title_start_index + 26 :line.find('<', title_start_index + 26)]
                    else:
                        title = line
                expect_title = False
                expect_directed_by = True
            elif expect_directed_by:
                directed_by = line[4:-5]
                expect_directed_by = False
                expect_written_by = True
            elif expect_written_by:
                written_by = line[4:-5].replace('&amp;', '&')
                expect_written_by = False
                expect_original_air_date = True
            elif expect_original_air_date:
                if line.find('Teleplay by') != -1:
                    continue
                found_published_updated = line.find('published updated">')
                if found_published_updated != -1:
                    year, month, day = map(int, line[found_published_updated + 19: found_published_updated + 29].split('-'))
                    original_air_date =  date(year, month, day)
                else:
                    try:
                        original_air_date = datetime.strptime(line[4:line.find('<', 5)], '%B %d, %Y').date()
                    except:
                        print "\n\n******\ncan't parse line (%s): %s\n*******\n\n" % (line_number, line)
                        print page + '\n\n'
                        raise
                expect_original_air_date = False
                print 'adding episode: total_episodes=%s, season=%s, episodes_for_this_season=%s, title=%s, original_air_date=%s' % (total_episodes, season, episodes_for_this_season, title, original_air_date)
                self.add_episode(total_episodes, season, episodes_for_this_season, title, original_air_date)

            if line.find('<td') != -1 and line.find('</td>') == -1:
                expect_td_tag_close = True

    def print_episdoes(self):
        for ep in self.episodes:
            print ep

    def update_last_seen_ep(self, number_in_series='LAST_PUBLISHED'):
        if number_in_series == 'LAST_PUBLISHED':
            for episode in self.episodes[::-1]:
                if not episode.is_in_future():
                    self.last_seen_ep = episode
                    break
        else:
            if type(number_in_series) != type(0):
                raise 'Must receive integer as argument...'
            self.last_seen_ep = self.episodes[number_in_series - 1]
        print 'updating last_seen_ep to episode: %s' % (self.last_seen_ep)
        self.pickle()

    def pickle(self):
        with open(string_utils.turn_to_valid_filename(self.name)+'.show', 'w+') as f:
            pickle.dump(self, f)

    def download_new_episodes(self, reparse=False):
        unseen_episdoes = self.episodes[int(self.last_seen_ep.number_in_series):]
        if unseen_episdoes == []:
            print '%s: No more episode... (maybe time to update from wiki (when a new season comes out)?/remove from list of shows?)\n' % (self.name)
            return
        downloadable_episodes = [ep for ep in unseen_episdoes if ep.is_downloadable()]
        if downloadable_episodes == []:
            next_ep = unseen_episdoes[0]
            next_ep_date = next_ep.original_air_date
            print '%s: No new episodes available for download.. next episode (%s) will air in %s days (%s)\n' % (self.name, next_ep.SiEj, (next_ep_date - date.today()).days, next_ep_date)
            return
        for episode in downloadable_episodes:
            search_string = '%s %s' % (self.name.replace("'", ""), episode.SiEj)
            print 'Searching torrent for "%s"..' % (search_string)
            try:
                link = get_magnet_link_from_pirate_bay(search_string)
                print 'Got magnet link! Adding to client..'
                self.last_seen_ep = episode
                self.pickle()
                add_to_client(link)
            except:
                print "Coundn't get magnet url... =\\"


def get_or_update_show_info(show_name, last_seen_ep='LAST_PUBLISHED'):
    show = Show(show_name)
    show.parse_episodes_list_from_wikipedia()
    show.update_last_seen_ep()
    show.pickle()

def update_shows(show_names):
    for show_name in show_names:
        get_or_update_show_info(show_name)

def load_shows(show_names):
    shows = []
    for show_name in show_names:
        with open (string_utils.turn_to_valid_filename(show_name)+'.show', 'r+') as f:
            shows.append(pickle.load(f))
    return shows

def print_episodes(show_names):
    shows = load_shows(show_names)
    for show in shows:
        print '\n\n' + show.name
        for episode in show.episodes:
            print '\t' + str(episode)

def print_last_seen_ep(show_names):
    shows = load_shows(show_names)
    for show in shows:
        print '\n%s - %s' % (show.name, show.last_seen_ep)

def download_new_episodes(show_names):
    shows = load_shows(show_names)
    for show in shows:
        print '\n\n' + show.name
        show.download_new_episodes()

if __name__ == '__main__':
    '''
    Usage: put the show names that you want in show_names.
           uncomment #update_shows(show_names)
           by default, on update_shows() the latest_unseen_ep will be synched to the latest aired episode, you can change it later manually with show.update_last_seen_ep(episode_number_in_series)
           Periodically run the program (crone job?). The loop of at the end (show.download_new_episodes()) will do the rest :)
           Once you update_shows() there's no need to querry wikipedia over and over, unless a new season starts and the new airdates are published
    '''

    #shows_waiting_for_next_season = ['House of Cards', 'bob\'s burgers', 'The Walking Dead', 'Family Guy', 'Brooklyn Nine-Nine', 'South Park']
    show_names = ['The Big Bang Theory', 'Parks and Recreation', 'game of thrones']
    # Wentworth, Orange is the New Black
    #get_or_update_show_info('South Park')
    shows = load_shows(show_names)
    for show in shows:
        show.download_new_episodes()