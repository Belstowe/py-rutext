"""A Russian text generator based on templating texts and word picking"""

__version__ = "0.3.0"

from WordDict.WordList import WordList
from WordDict.FormKeepers import CustomFormKeeper
import yaml
import os.path


def user_interact(db):
    print('Введите слова:')
    while True:
        print()
        word = input()
        if len(word) == 0:
            break
        tokens = word.split(sep=' ')
        name = tokens[0]
        tags = tokens[1:] if len(tokens) > 1 else ()
        db.insert(name, tags)

    print('Введите теги:')
    while True:
        print()
        tags = input()
        if len(tags) == 0:
            break
        print(db.get(*tags.split()))


def main():
    db = WordList()

    if os.path.isfile("forms.yaml") and os.path.isfile("tags.yaml"):
        with open("forms.yaml", mode='r', encoding='utf-8') as f:
            forms = yaml.load(f, yaml.Loader)
            if type(forms) == dict:
                for key, value in forms.items():
                    db.forms[key] = CustomFormKeeper(value)

        with open("tags.yaml", mode='r', encoding='utf-8') as f:
            tags = yaml.load(f, yaml.Loader)
            if type(tags) == dict:
                db.tags = tags

    try:
        user_interact(db)
    finally:
        with open("forms.yaml", mode='w', encoding='utf-8') as f:
            pairs = {}
            for key, value in db.forms.items():
                pairs[key] = value.to_dict()
            yaml.dump(pairs, f, indent=2, allow_unicode=True)

        with open("tags.yaml", mode='w', encoding='utf-8') as f:
            yaml.dump(db.tags, f, indent=2, allow_unicode=True)


if __name__ == '__main__':
    main()