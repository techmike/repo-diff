import urllib2
import argparse
import urlparse
from os.path import basename
from bs4 import BeautifulSoup

class RepoDiff(object):
    def __init__(self):
        self.url = None
        self.components = []
        self.packages = []
        self.temp_url = None
        self.url_list = []
        self.url_list_stage = []

    def set_repo_url(self, url):
        """
        Set url value
        :param url:
        :return:
        """
        self.url = url

    def get_repo_url(self):
        """
        Return url value
        :return:
        """
        return self.url

    def set_temp_url(self, url):
        """
        Set staging url
        :param url:
        :return:
        """
        self.temp_url = str(url)

    def get_temp_url(self):
        """
        Return staging url
        :return:
        """
        return self.temp_url

    def set_repo_components(self, component_name):
        """
        Set repo components
        :param component_name:
        :return:
        """
        self.components.append(component_name)

    def get_repo_components(self):
        """
        Return repo component value
        :return:
        """
        return self.components

    def set_repo_list(self, repurl):
        """
        Add value to repo url
        :param repurl:
        :return:
        """
        self.set_temp_url(repurl)
        self.url_list.append(self.temp_url)

    def set_repo_packages(self, package_name):
        """
        Add value to packages list
        :param package_name:
        :return:
        """
        self.packages.append(package_name)

    def get_repo_packages(self):
        """
        Return packages list
        :return:
        """
        return self.packages

    def spider_repo_links(self):
        """
        Crawl the urls and keep adding parent links to url_list
        :return:
        """
        for link in self.url_list:
            #print link
            soup = BeautifulSoup(urllib2.urlopen(link), 'lxml')
            for alink in soup.find_all('a'):
                href = alink.get('href')
                #print link
                if href.startswith('/'):
                    #print ('skip, most likely the parent folder -> ' + href)
                    pass
                elif href.startswith('?'):
                    #print 'skip, garbage -> ' + href
                    pass
                elif href.endswith('/'):
                    new_link = link + "/" + href
                    self.url_list.append(new_link)
                else:
                    if href.endswith('.deb'):
                        print 'The package name is ' + href
                        self.set_repo_packages(href)

            self.url_list.remove(link)

    def save_package_list(self):
        """
        Save package dictionary to file
        :return:
        """
        file = open("repo_list", "w")
        for line in self.packages:
            file.write(line)
            file.write('\n')
        file.flush()
        file.close()

def main():
    parser = argparse.ArgumentParser(description='Save a text copy of packages in a repo')
    parser.add_argument('--repo', dest='repo', help='Provide the repo name\n\nExample: ftp://archive.ubuntu.com/ubuntu/pool')
    parser.add_argument('--comp', dest='comp',  default='main', help='Provide the comp name\n\nExample: main,universe  Default:main')
    args = parser.parse_args()
    if args.repo:
        myrepo = RepoDiff()
        myrepo.set_repo_url(args.repo)

        for comp in args.comp.split(','):
            myrepo.set_repo_components(comp)

        #Check Repo URL and Components
        #print myrepo.get_repo_url()
        #print myrepo.get_repo_components()

        #Build initial list of urls
        for num_of_comp in myrepo.get_repo_components():
            myurl = myrepo.get_repo_url() + "/" + num_of_comp
            #print myurl
            myrepo.set_repo_list(myurl)

        myrepo.spider_repo_links()
        #myrepo.get_repo_packages()
        myrepo.save_package_list()


    else:
        print "Please provide a repo: --repo http://repo.example.com/pool/"
        parser.print_help()

if __name__ == "__main__":
    main()