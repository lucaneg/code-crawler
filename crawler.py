def init_crawler(action, limit, workdir):
    from crawlers.github import GitHubCrawler
    
    crawlers = {
        'github' : GitHubCrawler(limit, workdir),
    }
    
    if not action in crawlers:
        raise Exception('Unknown crawler: ' + action)
       
    return crawlers[action]

if __name__ == "__main__":
    import argparse
    import configparser
    import os
    
    available_crawlers = ['github']

    parser = argparse.ArgumentParser(description = 'Code crawler: retrieveing code for constructing test sets')
    parser.add_argument('crawler', 
                        metavar = 'crawler', 
                        type = str, 
                        help = 'the name of the crawler, one of: ' + str(available_crawlers), 
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
    crawler = init_crawler(args.crawler, args.limit, args.workdir)
    

    if args.config_template:
        crawler.dump_conf_template()
    else:
        if os.path.isfile(args.config):
            config = configparser.ConfigParser()
            config.read(args.config)
            crawler.read_conf(config)
        elif crawler.requires_config():
            raise Exception(args.config + ' does not exist')
            
        crawler.crawl()
