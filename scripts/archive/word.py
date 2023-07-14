"""
class Word:
    def __init__(self, lemma, main_description, other_description, example):
        self.lemma = lemma
        self.main_description= main_description
        self.other_description = other_description
        self.example = example
        self.declined_forms = None
    def __str__(self):
        return f"Word: {self.lemma}\n"+f"main_description: {self.main_description}\nother_description: {self.other_description}\nexample: {self.example}"

def main(args: argparse.Namespace) -> None:
    words = get_words(filename=args.filename, included_cols=DEFAULT_COLUMN_DICT)

    for w in words:
        print(w)
        input()
"""
