import crawlers.base_crawler as base

import requests
from bs4 import BeautifulSoup
import random
from tqdm import tqdm

class MvnRandom(base.Crawler):
    def __init__(self, limit, workdir):
        super().__init__(limit, workdir, False)

        # this the full maven repository
        self.mvn_base = 'https://repo1.maven.org/maven2/'

        # 'org' has the most jars
        mvn_org = self.mvn_base + 'org/'
        # 'com', 'io' and 'net' are pretty big as well
        mvn_com = self.mvn_base + 'com/'
        mvn_net = self.mvn_base + 'net/'
        mvn_io = self.mvn_base + 'io/'
        
        # bigger sub-repos are listed separately to have a bigger chance 
        # of immediately descend in those ones
        # 'org' is listed more times to increase the chance of hitting
        self.sources = [mvn_org, mvn_org, mvn_org, mvn_com, mvn_net, mvn_io, self.mvn_base]

    def page_links(self, page_url):
        result = []
        
        response = requests.get(page_url)
        if not response.ok:
            response.raise_for_status()
        
        for anchor in BeautifulSoup(response.content, features='html.parser').find_all('a', href = True):
            link = anchor['href']
            # a link is valid if it is a directory link, but not '../', or a jar link
            if link == '../' or link.endswith('-javadoc.jar') or link.endswith('-sources.jar'):
                continue
            if link.endswith('/') or link.endswith('.jar'):
                # other types of files (e.g. pom) are not interesting
                result.append(page_url + link) 
                
        return result
        
    def random_jar(self, base_url):
        links = self.page_links(base_url)

        while len(links) > 0:
            link = random.choice(links)

            if link.endswith('.jar'):
                return link
        
            # at this point, link is a folder
            inner = self.random_jar(link)
            if not inner:
                # link is a folder that does not lead to a jar file:
                # ignore it and try with a different link
                links.remove(link)
            else:
                # it is a jar file
                return inner
                
        return None
    
    def get_jar_url(self, base_url):
        result = self.random_jar(base_url)
        if result:
            return result[len(self.mvn_base):], result

        raise Exception('Scanning "' + base_url + '" did not lead to any jar file')

    def crawl(self):
        crawled = 0
        print('Will crawl ' + str(self.limit) + ' jars', flush = True)
        
        to_crawl = dict()
        for i in tqdm(range(self.limit), ascii = True, desc = 'Searching for jar files', unit = 'jar'):
            base_url = random.choice(self.sources)
            jar_name, jar_url = self.get_jar_url(base_url)
            to_crawl[jar_name] = jar_url
        print()
        
        for jar_name, jar_url in to_crawl.items():
            print('- ' + jar_name, end = '', flush = True)
            zip_response = requests.get(jar_url, stream = True)
            with open(self.make_file(jar_name), 'wb') as handle:
                for data in tqdm(zip_response.iter_content(), ascii = True, desc='  downloading'):
                    handle.write(data)
            print()

