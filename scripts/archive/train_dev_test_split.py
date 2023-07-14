####################################################
# TYHLE

# def __lemma_complex_to_raw(
#     lemma: InflectedLemmaFormsDict,
# ) -> InflectedLemmaFormsDict:
#     lemma.lemma = raw_lemma_from_lemma(lemma.lemma)
#     return lemma


# # GENERIC METHODS ###
# def __select_tags(
#     lemma: InflectedLemmaFormsDict, tag_selector: callable[[str], bool]
# ) -> InflectedLemmaFormsDict:
#     """
#     Expects tag
#     # Skip lemmata that are equal to the last lemma _selector to return true, if the given tag should be preserved,
#     false if it should be removed.
#     """
#     to_be_deleted = []
#     for tag in lemma.inflected_forms:
#         if not tag_selector(tag):
#             to_be_deleted.append(tag)
#     for tag in to_be_deleted:
#         del lemma.inflected_forms[tag]
#     return lemma


# # filter_lemmata_and_forms
# def __load_train_data() -> iter[InflectedLemma]:
#     """
#     Reads the raw morfflex file and turns it to iterator over InflectedLemmata.
#     The raw morfflex file should contain randomly shuffled rows, but the rows
#     containing the same lemma (or the same raw lemma) should appear
#     consecutively.
#     If 2 lemmata have the same raw lemma, they appear consecutively in
#     the result.
#     """
#     # Lemmata with all forms from morfflex
#     lemmata = __load_lemmata_with_all_forms(MORFFLEX_RAW)

#     # Convert complex_lemma to raw_lemma
#     lemmata = (__lemma_complex_to_raw(lemma) for lemma in lemmata)

#     # Lemmata with selected basic forms
#     lemmata = __apply_tag_selector(
#         lemmata, tag_selector=lambda tag: tag[-1] == "-"
#     )

#     # Remove negation forms
#     lemmata = __apply_tag_selector(
#         lemmata, tag_selector=lambda tag: tag[10] != "N"
#     )

#     # Simplify tags to contain only number and case flags.
#     lemmata = (__simplify_tags(lemma) for lemma in lemmata)

#     # Define allowed tags sets:
#     tags_singular = [f"S{i}" for i in range(1, 8)]
#     tags_plural = [f"P{i}" for i in range(1, 8)]
#     tags = tags_singular + tags_plural

#     taglists = [[], ["XX"], ["XX", "S1"], tags_singular, tags_plural, tags]
#     tagsets = [set(taglist) for taglist in taglists]

#     tags_set = set(tags)

#     # Removed lemmata with strange tag set
#     lemmata = filter(
#         lambda lemma: (set(lemma.inflected_forms) in tagsets), lemmata
#     )

#     # Complete tags and forms to the count of 14
#     lemmata = (__complete_tags(lemma, tags=tags_set) for lemma in lemmata)

#     # Convert dict{tag:form} to list[form]
#     lemmata = (
#         InflectedLemma(
#             lemma.lemma, [lemma.inflected_forms[tag] for tag in tags]
#         )
#         for lemma in lemmata
#     )
#     # TODO: write to file.
#     return lemmata

# # morfflex2formdict
# def __load_lemmata_with_all_forms(
#     filename: str,
# ) -> iter[InflectedLemmaFormsDict]:
#     """
#     Read raw morfflex and extract every lemma with a dict {tag: form}.
#     """
#     with open(filename, "r") as f:
#         last_lemma = ""
#         last_inflected_lemma = None
#         counter = 0
#         for line in f:
#             line = line.rstrip()
#             tokens = line.split(MORFFLEX_COLUMN_SEPARATOR)
#             (lemma, tag, form) = tuple(tokens)

#             if lemma != last_lemma:
#                 if (
#                     counter != 0
#                 ):
#                     # Ensure that None will not be yielded at the beginning
#                     yield last_inflected_lemma

#                 last_lemma = lemma
#                 last_inflected_lemma = InflectedLemmaFormsDict(lemma, {})
#                 counter += 1

#             last_inflected_lemma.inflected_forms[tag] = form

# def __apply_tag_selector(
#     lemmata: iter[InflectedLemmaFormsDict], tag_selector: callable[[str], bool]
# ) -> iter[InflectedLemmaFormsDict]:
#     modifier = lambda lemma: __select_tags(lemma, tag_selector)
#     return (modifier(lemma) for lemma in lemmata)


# # END OF GENERIC METHODS ###


# def __simplify_tags(lemma: InflectedLemmaFormsDict) -> InflectedLemmaFormsDict:
#     """
#     Simplify tags in the given lemma to contain only number and case flags.
#     """

#     def simplify_tags_in_dict(forms: dict[str, str]) -> dict[str, str]:
#         old_tags = list(forms.keys())

#         def simplify(tag: str) -> str:
#             return tag[3:5]

#         for old_tag in old_tags:
#             forms[simplify(old_tag)] = forms[old_tag]
#             del forms[old_tag]
#         return forms

#     lemma.inflected_forms = simplify_tags_in_dict(lemma.inflected_forms)
#     return lemma


# def __complete_tags(
#     lemma: InflectedLemmaFormsDict, tags: set[str]
# ) -> InflectedLemmaFormsDict:
#     def complete_tags_in_dict(
#         lemma: str, forms: dict[str, str], tags: set[str]
#     ) -> dict[str, str]:
#         old_tags = list(forms.keys())
#         count = len(old_tags)
#         if count == 0:
#             default_value = lemma
#             for tag in tags:
#                 forms[tag] = default_value
#         if count == 1:
#             old_tag = old_tags[0]
#             default_value = forms[old_tag]
#             del forms[old_tag]
#             for tag in tags:
#                 forms[tag] = default_value
#         if count == 2:
#             default_value = forms["XX"]
#             for old_tag in old_tags:
#                 del forms[old_tag]
#             for tag in tags:
#                 forms[tag] = default_value
#         if count == 7:
#             missing_tags = tags - set(old_tags)
#             for tag in missing_tags:
#                 forms[tag] = "?"
#         if count == 14:
#             # Nothing to complete
#             pass
#         return forms

#     lemma.inflected_forms = complete_tags_in_dict(
#         lemma.lemma, lemma.inflected_forms, tags
#     )
#     return lemma

# class InflectedLemmaFormsDict:
#     def __init__(
#         self, complex_lemma: str, inflected_forms: dict[str, str]
#     ) -> None:
#         self.lemma = complex_lemma
#         self.inflected_forms = inflected_forms

# #############################################################



# def build_train_dev_test_split_data(
#     train_tgt: str = TRAIN_DATA_FILE, 
#     dev_tgt: str = DEV_DATA_FILE, 
# #    dev_large_tgt: str = DEV_DATA_LARGE_FILE,
#     test_tgt: str = TEST_DATA_FILE
#     ) -> None:
#     """
#     Loads the whole available train data, splits it to the train, dev and test
#     parts and saves them to given files.

#     Expects the `__load_filtered_data` method to return Inflected lemmata in
#     a shuffled order, however, when they have the same raw lemma, they should 
#     appear consecutively. Otherwise, the zero-size intersection of the train
#     and the dev set (and the zero-size intersection of the train and the test
#     set) is not guaranteed.
#     """
#     print("Building the train, dev and test data...")

#     # TODO: vzhledem k tomu, ze tahle metoda uz mi vraci lemmata shufflovana,
#     # muzu tady proste vzit prvnich X jako test, dalsich X jako dev a pak
#     # nejakych Y jako train.
    
#     lemmata = __load_filtered_data()

#     train_lemmata = []
#     dev_lemmata = []
# #    dev_large_lemmata = []
#     test_lemmata = []

#     random.seed(42)

#     DatasetType = Enum('DatasetType', ['TRAIN', 'DEV', 'TEST'])
#     types = [DatasetType.TRAIN, DatasetType.DEV, DatasetType.TEST]
#     probs = [0.8, 0.1, 0.1]
#     last_rand_choice = None
#     last_raw_lemma = None

#     for lemma in lemmata:

#         raw_lemma = raw_lemma_from_lemma(lemma.lemma)
#         if (raw_lemma == last_raw_lemma):
#             # If the raw lemma is the same as the last one,
#             # add it to the same set.
#             rand_choice = last_rand_choice
#         else:
#             rand_choice = random.choices(types, probs)[0]

#         if (rand_choice == DatasetType.TRAIN):
#             # put 8/10 of the input lemmata to the train data
#             train_lemmata.append(lemma)
#         elif (rand_choice == DatasetType.DEV):
#             # put 1/10 of the input lemmata to the dev data
#             dev_lemmata.append(lemma)
#         #elif (rand_choice == DatasetType.DEV_LARGE):
#         #    # put 1/10 of the input lemmata to the dev data
#         #    dev_large_lemmata.append(lemma)
#         else:
#             # and the rest (1/10) to the test data
#             test_lemmata.append(lemma)

#         last_raw_lemma = raw_lemma
#         last_rand_choice = rand_choice

#     InflectedLemma.multiple_to_file(lemmata=train_lemmata, filename=train_tgt)
#     InflectedLemma.multiple_to_file(lemmata=dev_lemmata, filename=dev_tgt)
#     #InflectedLemma.multiple_to_file(lemmata=dev_large_lemmata, filename=dev_large_tgt)
#     InflectedLemma.multiple_to_file(lemmata=test_lemmata, filename=test_tgt)
