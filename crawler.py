import argparse
import configparser
import os
import fnmatch
import subprocess

from crawlers.github import GitHubCrawler
from crawlers.mvn_rand import MvnRandom

def any_match(path, filters):
    for f in filters:
        if fnmatch.fnmatch(path, f):
            return True
    return False
    
def normalize(path):
    return os.path.abspath(os.path.normpath(path))
   
def execute(cmd, param):
    pos = cmd.find('{}')
    if pos == -1:
        full = cmd + ' ' + param
    else:
        full = cmd.replace('{}', param)
    print('- executing: ' + full, flush = True)
    proc = subprocess.run(full)
    return proc.returncode == 0
    
def iterate(cmd, items_label, items, filtering = None):
    print('Executing "' + cmd + '" on ' + items_label, flush = True) 
    
    runs = 0
    succeeded = 0
    failed = 0
    for item in items:
        if not filtering or filtering(item):
            if execute(cmd, normalize(item)):
                succeeded += 1
            else:
                failed += 1
            runs += 1
    print('Execution completed (runs: ' + str(runs) + ', succeeded: ' + str(succeeded) + ', failed: ' + str(failed) + ')', flush = True)
    
if __name__ == "__main__":
    
    crawlers = {
        'github' : lambda limit, workdir, skip_existing : GitHubCrawler(limit, workdir, skip_existing),
        'mvn-rand' : lambda limit, workdir, skip_existing : MvnRandom(limit, workdir, skip_existing),
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
    parser.add_argument("-s", 
                        "--skip-existing", 
                        default = False, 
                        help = "when retrieving a crawled result, skip the retrieval it if it already exists in the workdir, but still consider it a crawled item (useful to avoid retrieving the same item in subsequent executions)", 
                        action = 'store_true'
                        )
    parser.add_argument("-t", 
                        "--config-template", 
                        help = "instead of executing, dump the configuration template for the given crawler to <workdir>/crawler.conf.template",
                        default = False,
                        action = 'store_true'
                        )
    parser.add_argument("-f", 
                        "--filter-files", 
                        metavar = 'filter',
                        type = str,
                        help = "comma separated list of globs (fnmatch style) for filtering crawled files in each crawled result for subsequent --fexec (if no --fexec is provided, this option is useless) - wrap them in double quotes to avoid glob expansion in your terminal",
                        default = "",
                        )
    parser.add_argument("-e", 
                        "--exec", 
                        metavar = 'command',
                        type = str,
                        help = "command to execute on each crawled result; absolute path to the result - file or folder - will be replaced to all occurrences of '{}', or appendend at the end of the command if no occurrence is found",
                        default = "",
                        )
    parser.add_argument("-x", 
                        "--fexec", 
                        metavar = 'command',
                        type = str,
                        help = "command to execute on each file (optionally filtered with --filter-files) inside each crawled result; absolute path to the result - file or folder - will be replaced to all occurrences of '{}', or appendend at the end of the command if no occurrence is found",
                        default = "",
                        )
    
    args = parser.parse_args()
    
    if not args.crawler in available_crawlers:
        raise Exception('Unknown crawler: ' + action)
        
    crawler = crawlers[args.crawler](args.limit, args.workdir, args.skip_existing)

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
        
    result = crawler.crawl()
    
    print('Crawling completed', flush = True) 
    
    if args.exec:
        iterate(args.exec, 'all clrawled result', result)
    elif args.fexec:
        files = []
        for crawled in result:
            if os.path.isdir(crawled):
                for dirpath, subdirs, filelist in os.walk(crawled):
                    for name in filelist:
                        files.append(normalize(os.path.join(dirpath, name)))
            else: 
                files.append(normalize(crawled))
        if args.filter_files:
            filters = args.filter_files.split(',')
            iterate(args.fexec, 'individual clrawled files that match one of "' + str(filters) + '"', files, lambda item : any_match(item, filters))
        else:
            iterate(args.fexec, 'all individual clrawled files', files)
