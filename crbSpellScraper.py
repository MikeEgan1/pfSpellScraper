from bs4 import BeautifulSoup
import urllib2

def main():
    url = "http://paizo.com/pathfinderRPG/prd/coreRulebook/spellLists.html"
    content = urllib2.urlopen(url)
    soup = BeautifulSoup(content.read(), "html.parser")
    for x in soup.find_all('p'):
        for y in x.find_all('b'):
            links = y.find_all('a')
            if len(links) > 0:
                spell = links[0]
                parse_spell(spell.get('href'), spell.text)

def parse_spell(url, spell_name):
    print url
    print spell_name

if __name__ == "__main__":
    main()