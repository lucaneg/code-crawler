import os
import shutil

class Crawler:
    def __init__(self, limit, workdir, needs_config):
        self.limit = limit
        self.workdir = workdir
        self.needs_config = needs_config
        
        if os.path.isdir(self.workdir):
            ans = input('Caution: selected warning directory \'' + self.workdir + '\' already exists, delete it? [y/n] ')
            if ans.lower() == 'y' or ans.lower() == 'yes':
                shutil.rmtree(self.workdir, ignore_errors = True)
            else:
                print('Cannot continue: workdir alreay exists and answer was: ' + ans)
                exit()
                
        os.makedirs(self.workdir)
        
    def read_conf(self, config):
        raise Exception('No read_conf method provided by ' + type(self).__name__)
        
    def crawl(self):
        raise Exception('No crawl method provided by ' + type(self).__name__)
        
    def requires_config(self):
        return self.needs_config
        
    def dump_conf_template(self):
        if not self.needs_config:
            print(type(self).__name__ + ' does not need a configuration')
        else:
            raise Exception('No dump_conf_template method provided by ' + type(self).__name__)
            