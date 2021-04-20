import os
import shutil

class Crawler:
    def __init__(self, limit, workdir, needs_config):
        self.limit = limit
        self.workdir = workdir
        self.needs_config = needs_config
        
    def make_file(self, path):
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
            