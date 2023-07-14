"""
def build_all_train_data(tgt: str = TRAIN_DATA_FILE) -> None:
    
    Loads the train data and saves it to given file.
    
    print("Building the train data...")

    lemmata = __load_train_data()
    InflectedLemma.multiple_to_file(lemmata=lemmata, filename=tgt)
"""
