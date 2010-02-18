#!/usr/bin/env python
"""
Simulate a browser.

Login to google appengine, parse several web pages into data structures 
and return them to the caller.
"""

import re
import random
import logging
import logging.handlers
from BeautifulSoup import BeautifulSoup
from ClientForm import *
from mechanize import Browser

class SoupLoginError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class GoogleSoup:

    def __init__(self, username, password, logSeverity=logging.INFO):
        LOG_FILENAME = '/tmp/soup.out'

        # Set up a specific logger with our desired output level
        self.log = logging.getLogger('google_soup')
        self.log.setLevel( logSeverity )

        self.username = username
        self.password = password

        # Add the log message handler to the logger
        handler = logging.handlers.RotatingFileHandler( LOG_FILENAME, maxBytes=20, backupCount=5)
        self.log.addHandler(handler)

        self.br = Browser()

    def login(self, username, password):
        self.username = username
        self.password = password
        self.br.open("http://appengine.google.com/")
        self.br.select_form(nr=0)
        # sometimes google "suggests" a email and requires us to put the
        # password in for it
        if self.br["Email"] is None or self.br["Email"] == '':
            self.br["Email"] = username
        self.br["Passwd"] = password
        response = self.br.submit()
        page_title = self.br.title()
        self.log.debug('On web Page %s, %s' % (response.geturl(), page_title))
        self.ensureMainPage()
        return response

    def ensureMainPage(self):
        page_title = self.br.title()
        self.log.debug('On web Page %s' % (page_title))
        if page_title == 'Google Accounts' or page_title != 'Applications Overview':
                raise SoupLoginError(self.username)

    def resetClient(self):
        return self.login(self.username, self.password)

    def strip_tags(self, element):
        text_accumulator = element.contents[0]
        for tag in element.findAll():
            tag_text = tag.renderContents()
            text_accumulator += tag_text
        text_accumulator = re.sub('\n', ' ', text_accumulator)
        text_accumulator = re.sub('&nbsp;', ' ', text_accumulator)
        text_accumulator = text_accumulator.strip()
        return text_accumulator

    def extract_headings(self, table):
        table_headings = []
        for header in table.findAll('th'):
            text = self.strip_tags(header)
            table_headings.append(text)
        return table_headings

    def findApplications(self):
        main_apps = BeautifulSoup(self.resetClient())
        column_headers = []
        apps = []
        for table in main_apps.findAll('table', limit=1):
            # table is a BeautifulSoup.Tag object
            column_headers = self.extract_headings(table)

            for app_row in table.tbody.findAll('tr'):
                column = 0
                basic_app_data = {}

                for app_data in app_row.findAllNext('td', limit=len(column_headers)):
                    data_value = app_data.renderContents()
                    attribute_name = column_headers[column]
                    if 'app_id' in data_value:
                        app_link = app_data.find('a', href=re.compile('.*app_id='))
                        app_url = app_link['href'] #.attrs
                        app_link.renderContents()
                        basic_app_data.update({'url':app_url})
                        basic_app_data.update({'name':self.strip_tags(app_data)})
                    if 'ae-ext-link' in data_value:
                        data_value = self.strip_tags(app_data)

                    basic_app_data.update({attribute_name:data_value})
                    column += 1

                apps.append(basic_app_data)

        return apps

    def decompose_reservation(self, stat_name, usage):
        usage = re.sub('\n', ' ', usage)
        if ' of ' in usage:
            parts = re.search('([0-9\.]*).of.([0-9\.]*)([^ ]*.*)', usage, re.MULTILINE)
            if parts:
                used, remaining, metric = parts.groups()
                metric = metric or stat_name
                return { 'metric': metric, 'used':used, 'remaining':remaining }
            else:
               return None

    def queryApplicationPerfs(self, applicationNames):
        self.resetClient()
        if applicationNames == '__ALL__':
            applicationLinks =  self.br.links(url_regex='app_id=')
        else:
            for applicationName in applicationNames:
                applicationLinks =  self.br.find_link(url_regex='app_id=%s' % applicationName)

        quota_stats = {}
        self.log.debug( 'Looking for application %s ' % applicationNames)
        for applicationLink in applicationLinks:
            response = self.br.follow_link(applicationLink)
            response = self.br.follow_link(text_regex=r'Quota Details')
            current_url = response.geturl()
            app_id_match = re.search('app_id=([^&]*)', current_url)
            if app_id_match:
                app_id = app_id_match.groups()[0]
            else:
                app_id = 'unknown_app'
            self.log.debug('Taking stats for application %s ' % app_id)
            quota_stats[app_id] = {}
            quota_details = response.read()
            quota_fix = re.compile('.*Why is My App Over Quota', re.DOTALL|re.MULTILINE)
            quota_details = re.sub(quota_fix, '', quota_details)
            quota_soup = BeautifulSoup(quota_details)
            quota_section = quota_soup.find(attrs={'id':'ae-quota-details'})
            if quota_section:
                for quota_table in quota_section.findAll('table'):
                        for stat_row in quota_table.tbody.findAll('tr', recursive=False):
                            stat_name = self.strip_tags(stat_row.find('td'))
                            for usage in stat_row.findAll('td', text=re.compile('%')):
                                usage_string = usage.strip('\n')
                                usage_string = int(usage_string.rstrip('%'))
                                reservation = self.strip_tags(usage.parent.findNextSibling())
                                reservation_components = self.decompose_reservation(stat_name, reservation)
                                # just send random stuff for testing!!!!
                                usage_string = str(random.randint(1000, 100000))
                                quota_stats[app_id][stat_name + '_usage'] = usage_string
                                quota_stats[app_id][stat_name + '_quota'] = reservation_components['used']
                                quota_stats[app_id][stat_name + '_remaining'] = reservation_components['remaining']
        return quota_stats

    def parse_load(self):
        app_main = open('/tmp/dashboard.html', 'r').read()
        app_soup = BeautifulSoup(app_main)
        load_section = app_soup.find(text=re.compile('Current Load'))
        current_load = []
        if load_section:
            load_section = load_section.findParent('table')
            if load_section:
                column_headers = self.extract_headings(load_section)
                column = 0

                for stat_row in load_section.findAll('tr'):
                    load_data = {}

                    column = 0
                    for stat_data in stat_row.findAll('td', limit=len(column_headers)):
                        stat_name = column_headers[column]
                        column += 1
                        if 'URI' in stat_name:
                            load_data['uri'] = stat_data.find('a')
                            load_data['name'] = stat_data.find('a').string
                        else:
                            load_data[stat_name] = self.strip_tags(stat_data)
                    current_load.append(load_data)


    def parse_errors(self):
        errors_section = app_soup.find(id='ae-dash-errors-count-col')
        errors = []
        if errors_section:
            errors_section = errors_section.findParent('table')
            if errors_section:
                column_headers = self.extract_headings(errors_section)
                column = 0

                for stat_row in errors_section.findAll('tr'):
                    error_data = {}

                    column = 0
                    for stat_data in stat_row.findAll('td', limit=len(column_headers)):
                        stat_name = column_headers[column]
                        column += 1
                        if 'URI' in stat_name:
                            error_data['uri'] = stat_data.find('a')
                            error_data['name'] = stat_data.find('a').string
                        else:
                            error_data[stat_name] = self.strip_tags(stat_data)
                    errors.append(error_data)
        self.log.error(errors)

if __name__ == '__main__':
        pass
        # for testing
        # g = GoogleSoup('username', 'password')
        # print g.findApplications()
