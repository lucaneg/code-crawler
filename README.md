# code-crawler

A python crawler to download code from various sources to easily build test sets.

## Setup
- **python3**
- additional python packages to install through `pip install`: 
	- `requests`
	- `configparser`
	- `tqdm`
	- `gitpython`
	- `BeautifulSoup4`
- alternatively, you can use `pipreqs` (installable with `pip install pipreqs`), running from the root folder of the repo: `pipreqs . | pip install -r requirements.txt`

## Run

The only mandatory parameter is the name of the crawler. The available crawlers can be displayed through the help message:

```
$ python crawler.py github -h
usage: crawler.py [-h] [-c path] [-l n] [-d path] [-t] [-f filter]
                  [-e command] [-x command]
                  crawler

Code crawler: retrieveing code for constructing test sets

positional arguments:
  crawler               the name of the crawler, one of: github, mvn-rand

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
  -f filter, --filter-files filter
                        comma separated list of globs (fnmatch style) for
                        filtering crawled files in each crawled result for
                        subsequent --fexec (if no --fexec is provided, this
                        option is useless) - wrap them in double quotes to
                        avoid glob expansion in your terminal
  -e command, --exec command
                        command to execute on each crawled result; absolute
                        path to the result - file or folder - will be replaced
                        to all occurrences of '{}', or appendend at the end of
                        the command if no occurrence is found
  -x command, --fexec command
                        command to execute on each file (optionally filtered
                        with --filter-files) inside each crawled result;
                        absolute path to the result - file or folder - will be
                        replaced to all occurrences of '{}', or appendend at
                        the end of the command if no occurrence is found
```

Other options are used to tune general parameters that are not crawler-dependent: the working directory, the maximum number of results and the path to the crawler configuration.

Glob matching is performed through [fnmatch](https://docs.python.org/3/library/fnmatch.html#module-fnmatch).

### Crawler-specific configuration

Each crawler might require additional parameters that can be provided through a configuration file. Execute `python crawler.py <crawler> -t` to generate a `crawler.conf.template`
containing the configuration template to be filled and passed to the next execution with `-c`.