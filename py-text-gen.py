"""A text generator based on templating texts and word picking"""

__version__ = "0.2"

from WordDict.WordList import WordList
import yaml


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
    
    with open("forms.yaml", mode='w', encoding='utf-8') as f:
        pairs = []
        for key, value in db.forms.items():
            pairs.append({key: value.to_dict()})
        yaml.dump(pairs, f, indent=2, allow_unicode=True)

    with open("tags.yaml", mode='w', encoding='utf-8') as f:
        yaml.dump(db.tags, f, indent=2, allow_unicode=True)

if __name__ == '__main__':
    main()