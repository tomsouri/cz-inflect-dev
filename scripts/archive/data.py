
# def get_dev_data_large(max_size: int = inf) -> list[InflectedLemma]:
#     """
#     Returns list of dev data.
#     """
#     if not os.path.exists(DEV_DATA_LARGE_FILE):
#         build_train_dev_test_split_data(
#             dev_large_tgt=DEV_DATA_LARGE_FILE
#             )
#     return list(
#         __get_data(
#             filename=DEV_DATA_LARGE_FILE,
#             max_size=max_size,
#         )
#     )

if __name__ == "__main__":
    #train_data = get_train_data()
    # convert2neural_format(train_data, "neural.src", "neural.tgt")
    #convert2neural_format(get_dev_data(), "dev.src", "dev.tgt")
    #convert2neural_format(get_test_data(), "test.src", "test.tgt")

    """
    train_data = [lemma.lemma for lemma in get_train_data()]
    dev_data = [lemma.lemma for lemma in get_dev_data()]
    test_data = [lemma.lemma for lemma in get_test_data()]
    train_data = set(train_data)
    dev_data = set(dev_data)
    test_data = set(test_data)

    print(f"Intersection of train and dev: {len(train_data & dev_data)}")
    print(f"Intersection of train and test: {len(train_data & test_data)}")
    print(f"Intersection of test and dev: {len(test_data & dev_data)}")
    
    counter = 0
    for x in train_data & dev_data:
        print(x)
        input()
        counter += 1
        if counter == 10:
            break
    """

