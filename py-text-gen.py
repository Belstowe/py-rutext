"""A text generator based on templating texts and word picking"""

__version__ = "0.1"

from WordDict.WordList import WordList

def main():
    db = WordList()
    tokens = input().split(sep=' ')
    name = tokens[0]
    tags = tokens[1:]
    db.insert(name, tags)

if __name__ == '__main__':
    main()