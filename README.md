# code-crawler

A python crawler to download code from various sources to easily build test sets.

## Setup
- **python3**
- additional python packages to install through `pip3 install`: `requests`, `configparser`, `tqdm`, `gitpython`

## Run

The only mandatory parameter is the name of the crawler. The available crawlers can be displayed through the help message:

```
$ python crawler.py -h
usage: crawler.py [-h] [-c path] [-l n] [-d path] [-t] crawler

Code crawler: retrieveing code for constructing test sets

positional arguments:
  crawler               the name of the crawler, one of: <available crawlers>

optional arguments:
  -h, --help            show this help message and exit
  -c path, --config path
                        path to the configuration file, defaults to
                        'crawler.conf'
  -l n, --limit n       maximum number of returned results, defaults to 100
  -d path, --workdir path
                        path to the working directory, defaults to
                        'crawl_result'
  -t, --config-template
                        instead of executing, dump the configuration template
                        for the given crawler to
                        <workdir>/crawler.conf.template
```

Other options are used to tune general parameters that are not crawler-dependent: the working directory, the maximum number of results and the path to the crawler configuration.

### Crawler-specific configuration

Each crawler might require additional parameters that can be provided through a configuration file. Execute `python crawler.py <crawler> -t` to generate a `crawler.conf.template`
containing the configuration template to be filled and passed to the next execution with `-c`.