import crawlers.base_crawler as base

import requests
import json
import os
from distutils.util import strtobool
from git import Repo
from tqdm import tqdm

class GitHubCrawler(base.Crawler):
    def __init__(self, limit, workdir):
        super().__init__(limit, workdir, True)
        
    def dump_conf_template(self):
        template = '''[crawler]
# github username
user = 
# github access token (see https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token)
token = 
# whether or not matching repositories should be cloned inside the working directory
clone = false
# whether or not matching repositories should be downloaded as zip files inside the working directory
zip = false

[query]
# main search query
query = 

# search parameters, each matching one of the parameters in 
# https://docs.github.com/en/github/searching-for-information-on-github/searching-for-repositories

# restrict search to (comma-separated list): name, description, readme
in = 

# search for a specific owner
user = 
org = 

# properties of the repository
language = 
topic = 
license = 
fork = 
mirror = 
archived = 
followers = 
forks = 
stars = 
topics = 
created = 
pushed = 
'''
        with open(os.path.join(self.workdir, 'crawler.conf.template'), 'w') as f:
            f.write(template)
        
    def read_conf(self, config):
        self.crawler_user = config['crawler']['user']
        self.crawler_token = config['crawler']['token']
        self.crawler_clone = bool(strtobool(config['crawler']['clone']))
        self.crawler_zip = bool(strtobool(config['crawler']['zip']))

        
        self.query_query = config['query']['query']
        self.query_in = config['query']['in']
        self.query_user = config['query']['user']
        self.query_org = config['query']['org']
        self.query_language = config['query']['language']
        self.query_topic = config['query']['topic']
        self.query_license = config['query']['license']
        self.query_fork = config['query']['fork']
        self.query_mirror = config['query']['mirror']
        self.query_archived = config['query']['archived']
        self.query_followers = config['query']['followers']
        self.query_forks = config['query']['forks']
        self.query_stars = config['query']['stars']
        self.query_topics = config['query']['topics']
        self.query_created = config['query']['created']
        self.query_pushed = config['query']['pushed']
        
    def query(self, url):
        response = requests.get(url, auth=(self.crawler_user, self.crawler_token))

        if response.ok:
            return response
        else:
            response.raise_for_status()

    def build_query(self):
        query = 'https://api.github.com/search/repositories?q='

        if self.query_query:
            query += self.query_query + '+'
        if self.query_in:
            query += 'in:' + self.query_in + '+'
        if self.query_user:
            query += 'user:' + self.query_user + '+'
        if self.query_org:
            query += 'org:' + self.query_org + '+'
        if self.query_language:
            query += 'language:' + self.query_language + '+'
        if self.query_topic:
            query += 'topic:' + self.query_topic + '+'
        if self.query_license:
            query += 'license:' + self.query_license + '+'
        if self.query_fork:
            query += 'fork:' + self.query_fork + '+'
        if self.query_mirror:
            query += 'mirror:' + self.query_mirror + '+'
        if self.query_archived:
            query += 'archived:' + self.query_archived + '+'
        if self.query_followers:
            query += 'followers:' + self.query_followers + '+'
        if self.query_forks:
            query += 'forks:' + self.query_forks + '+'
        if self.query_stars:
            query += 'stars:' + self.query_stars + '+'
        if self.query_topics:
            query += 'topics:' + self.query_topics + '+'
        if self.query_created:
            query += 'created:' + self.query_created + '+'
        if self.query_pushed:
            query += 'pushed:' + self.query_pushed + '+'

        if query.endswith('+'):
            query = query[:-1]
        query += '&sort=stars&order=desc&per_page=100&page=1'

        return query

    def crawl(self):
        print('Preparing query...', flush = True)
        url = self.build_query()
        print('Invoking GitHub APIs...', flush = True)
        response = self.query(url)
        result = json.loads(response.content.decode('utf-8'))

        matching = int(result['total_count'])
        to_crawl = min(self.limit, matching)
        print('Matching projects: ' + str(matching))
        print('Crawling up to: ' + str(to_crawl), flush = True)
        
        if to_crawl == 0:
            print('Nothing to crawl: exiting')
            exit()

        repos = list()
        next_page = True
        while next_page and len(repos) <= to_crawl:
            for repo in result['items']:
                if len(repos) <= to_crawl:
                    repos.append(repo)
                else: 
                    break
                    
            if 'next' in response.links and len(repos) < to_crawl:
                url = response.links['next']['url']
                response = query(url)
                result = json.loads(response.content.decode('utf-8'))
            else:
                next_page = False
                
        for repo in repos:
            print('- ' + repo['full_name'], flush = True)

            if self.crawler_clone:
                print('  cloning...', flush = True)
                Repo.clone_from(repo['clone_url'], os.path.join(self.workdir, repo['full_name']))

            if self.crawler_zip:
                print('  downloading...', flush = True)
                zip_url = 'https://github.com/' + repo['full_name'] + '/archive/master.zip'
                zip_response = requests.get(zip_url, stream = True)
                full_path = os.path.join(self.workdir, repo['full_name'].split('/')[0])
                if not os.path.exists(full_path):
                    os.makedirs(full_path)
                with open(os.path.join(self.workdir, repo['full_name'] + '.zip'), 'wb') as handle:
                    for data in tqdm(zip_response.iter_content()):
                        handle.write(data)

