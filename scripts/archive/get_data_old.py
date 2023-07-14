"""
def get_dev_data(max_size: int = inf) -> list[InflectedLemma]:
    #Loads the evaluation data and returns them as a list of correctly inflected InflectedLemma.

    if not os.path.exists(DEV_DATA_FILE):
        build_dev_data(tgt=DEV_DATA_FILE)
    dev_data = InflectedLemma.multiple_from_file(DEV_DATA_FILE)
    counter = 0
    for lemma in dev_data:
        if counter >= max_size:
            break
        yield lemma
        counter += 1

def get_train_data(max_size: int = inf) -> list[InflectedLemma]:
    if not os.path.exists(TRAIN_DATA_FILE):
        build_train_data(tgt=TRAIN_DATA_FILE)
    train_data = InflectedLemma.multiple_from_file(TRAIN_DATA_FILE)
    counter = 0
    for lemma in train_data:
        if counter >= max_size:
            break
        yield lemma
        counter += 1
"""
# get_train_data = lambda max_size=inf : __get_data(filename=TRAIN_DATA_FILE, build_data=build_train_data, max_size=max_size)
# get_dev_data = lambda max_size=inf : __get_data(filename=DEV_DATA_FILE, build_data=build_dev_data, max_size=max_size)
