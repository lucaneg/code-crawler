import argparse
import configparser
import os

from crawlers.github import GitHubCrawler
from crawlers.mvn_rand import MvnRandom

if __name__ == "__main__":
    
    crawlers = {
        'github' : lambda limit, workdir : GitHubCrawler(limit, workdir),
        'mvn-rand' : lambda limit, workdir : MvnRandom(limit, workdir),
    }
    
    available_crawlers = crawlers.keys()

    parser = argparse.ArgumentParser(description = 'Code crawler: retrieveing code for constructing test sets')
    parser.add_argument('crawler', 
                        metavar = 'crawler', 
                        type = str, 
                        help = 'the name of the crawler, one of: ' + ', '.join(available_crawlers), 
                        choices = available_crawlers
                        )
    parser.add_argument("-c", 
                        "--config", 
                        metavar = 'path', 
                        type = str, 
                        help = "path to the configuration file, defaults to 'crawler.conf'", 
                        default = 'crawler.conf'
                        )
    parser.add_argument("-l", 
                        "--limit", 
                        metavar = 'n', 
                        type = int, 
                        help = "maximum number of returned results, defaults to 100", 
                        default = 100
                        )
    parser.add_argument("-d", 
                        "--workdir", 
                        metavar = 'path', 
                        type = str, 
                        help = "path to the working directory, defaults to 'crawl_result'", 
                        default = 'crawl_result'
                        )
    parser.add_argument("-t", 
                        "--config-template", 
                        help = "instead of executing, dump the configuration template for the given crawler to <workdir>/crawler.conf.template",
                        default = False,
                        action = 'store_true'
                        )
    
    args = parser.parse_args()
    
    if not args.crawler in available_crawlers:
        raise Exception('Unknown crawler: ' + action)
        
    crawler = crawlers[args.crawler](args.limit, args.workdir)

    if args.config_template:
        if crawler.requires_config():
            template_loc = crawler.dump_conf_template()
            print('Configuration template dumped to: ' + template_loc)
        else:
            print('Crawler ' + args.crawler + ' does not need a configuration')
        exit()
    
    if crawler.requires_config():
        if os.path.isfile(args.config):
            config = configparser.ConfigParser()
            config.read(args.config)
            crawler.read_conf(config)
        else:
            raise Exception(args.config + ' does not exist')
        
    crawler.crawl()
    
    print('Crawling completed') 
