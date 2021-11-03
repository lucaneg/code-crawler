import os
import shutil

class Crawler:
    def __init__(self, limit, workdir, needs_config):
        """Creates the crawler.
        
        Parameters:
        - limit:        the maximum number of entries to crawl
        - workdir:      where to store the crawled entries
        - needs_config: whether or not this crawler needs a configuration file
                        to run
        """
        
        self.limit = limit
        self.workdir = workdir
        self.needs_config = needs_config
        self.conf_template_filename = 'crawler.conf.template'
        
    def make_file(self, path):
        """Creates a file or directory at the given path, relative to the workdir. 
        
        All missing directories along the path are created recursively.
        If the file or directory already exists, the user is prompted for deletion.
        
        Parameters:
        - path: the path, relative to the workdir, of the file or directory to create
        """
        
        if not os.path.isdir(self.workdir):
            os.makedirs(self.workdir)
            
        target = os.path.join(self.workdir, path)
        if os.path.exists(target):
            ans = input('\'' + target + '\' already exists, delete it? [y/n] ')
            if ans.lower() == 'y' or ans.lower() == 'yes':
                if os.path.isdir(target) and not os.path.islink(target):
                    shutil.rmtree(target)
                else:
                    os.remove(target)
            else:
                print('Aborting...')
                exit()
        else:
            os.makedirs(os.path.dirname(target), exist_ok = True)
           
        return target
        
    def read_conf(self, config):
        """Reads the configuration for this crawler.
        
        Parameters:
        - config: the path to the configuration file
        """
        
        raise Exception('No read_conf implementation provided by ' + type(self).__name__)
        
    def crawl(self):
        """Performs the crawling. This method returns a list of paths, containing only the crawled results that have been stored on the file system.
        """
        
        raise Exception('No crawl implementation provided by ' + type(self).__name__)
        
    def requires_config(self):
        """Yields whether or not this crawler needs a configuration file.
        """
        
        return self.needs_config
        
    def dump_conf_template(self):
        """Dumps the configuration template for this crawler, only if needed, in a file named crawler.conf.template.
        """
        
        if not self.needs_config:
            print(type(self).__name__ + ' does not need a configuration')
        else:
            raise Exception('No dump_conf_template implementation provided by ' + type(self).__name__)
            