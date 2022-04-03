"""A text generator based on templating texts and word picking"""

__version__ = "0.1"

from WordDict.WordList import WordList

def main():
    db = WordList()
    tokens = input().split(sep=' ')
    name = tokens[0]
    args = tokens[1:]
    db.insert(name, args)

if __name__ == '__main__':
    main()