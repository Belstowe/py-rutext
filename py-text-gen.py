"""A text generator based on templating texts and word picking"""

__version__ = "0.1"

from WordDict.WordList import WordList

def main():
    db = WordList()
    print('Вводите слова:')
    while True:
        print()
        word = input()
        if len(word) == 0:
            break
        tokens = word.split(sep=' ')
        name = tokens[0]
        tags = tokens[1:] if len(tokens) > 1 else ()
        db.insert(name, tags)

    print('Вводите тэги:')
    while True:
        print()
        tags = input()
        if len(tags) == 0:
            break
        print(db.get(*tags.split()))

if __name__ == '__main__':
    main()