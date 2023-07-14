#!/usr/bin/env python3.9

# example call: .venv/bin/python3
# src/czech_inflection/dev_testing/eval_models/evaluate_onmt_model.py --name
# "First onmt model" --pred data/log/evaluate_models/onmt/EXAMPLE_FILE.txt

from __future__ import annotations

from dev_testing.eval_models.evaluate_onmt_model import evaluate_model
import argparse

import matplotlib.pyplot as plt


parser = argparse.ArgumentParser()
parser.add_argument(
    "--name",
    default="UnknownOnmtModel",
    type=str,
    help="Description of the model",
)

parser.add_argument(
    "--dev_pred",
    default="unknown_file.pred",
    type=str,
    help="The prefix of the files containg the dev predictions of the models",
)
parser.add_argument(
    "--train_pred",
    default=None,
    type=str,
    help="The prefix of the files containg the train predictions of the models",
)
parser.add_argument(
    "--every",
    default=1000,
    type=int,
    help="Every X steps the model was saved.",
)
parser.add_argument(
    "--max_steps",
    default=20000,
    type=int,
    help="Maximal number of training steps.",
)

parser.add_argument(
    "--dev_gold",
    default=None,
    type=str,
    help="The file containg the gold predictions on dev",
)

parser.add_argument(
    "--train_gold",
    default=None,
    type=str,
    help="The file containg the gold predictions on train",
)

parser.add_argument(
    "--logdir",
    default=None,
    type=str,
    help="Directory to print logs",
)


def main(args):
    possible_steps = list(range(args.every, args.max_steps + 1, args.every))
    dev_form_accs = []
    dev_lemma_accs = []

    train_form_accs = []
    train_lemma_accs = []

    for steps in possible_steps:
        prediction_filename = args.dev_pred + str(steps)

        accs = evaluate_model(
            model_name=args.name,
            pred_filename=prediction_filename,
            gold_filename=args.dev_gold,
        )
        dev_form_accs.append(accs[0].value)
        dev_lemma_accs.append(accs[1].value)

        if args.train_pred is not None:
            prediction_filename = args.train_pred + str(steps)
            accs = evaluate_model(
                model_name=args.name,
                pred_filename=prediction_filename,
                gold_filename=args.train_gold,
            )
            train_form_accs.append(accs[0].value)
            train_lemma_accs.append(accs[1].value)

    filename_full = args.logdir + "/training_accs.jpg"

    plot_accs(
        possible_steps,
        dev_form_accs=dev_form_accs,
        dev_lemma_accs=dev_lemma_accs,
        train_form_accs=train_form_accs,
        train_lemma_accs=train_lemma_accs,
        filename=filename_full,
    )

    filename_last_10_points = args.logdir + "/training_accs_last10.jpg"
    last_k = 10
    plot_accs(
        possible_steps[-last_k:],
        dev_form_accs=dev_form_accs[-last_k:],
        dev_lemma_accs=dev_lemma_accs[-last_k:],
        train_form_accs=train_form_accs[-last_k:],
        train_lemma_accs=train_lemma_accs[-last_k:],
        filename=filename_last_10_points,
    )

    # Write the training accuracies to a file
    def printout(file_handler, strings):
        file_handler.write(" ".join(f"{x:>16}" for x in strings) + "\n")

    with open(args.logdir + "training_accs.txt", "w") as f:
        # Print header
        output_strings = [
            "Training steps",
            "Dev form acc",
            "Dev lemma acc",
            "Train form acc",
            "Train lemma acc",
        ]
        printout(f, output_strings)

        for (steps, dev_form, dev_lemma, train_form, train_lemma, i) in zip(
            possible_steps,
            dev_form_accs,
            dev_lemma_accs,
            train_form_accs,
            train_lemma_accs,
            range(len(dev_form_accs)),
        ):
            output_strings = [str(steps)] + [
                f"{'!! ' if x >= max(xs) else '+ ' if x >= max(xs[:i+1]) else ''}{x:.8f}"
                for (x, xs) in zip(
                    [dev_form, dev_lemma, train_form, train_lemma],
                    [
                        dev_form_accs,
                        dev_lemma_accs,
                        train_form_accs,
                        train_lemma_accs,
                    ],
                )
            ]
            printout(f, output_strings)


def plot_accs(
    x_axis,
    dev_form_accs,
    dev_lemma_accs,
    train_form_accs,
    train_lemma_accs,
    filename,
):
    possible_steps = x_axis
    # plotting the form accs

    plt.figure(figsize=(40, 35))

    plt.plot(possible_steps, dev_form_accs, "-o", label="dev form acc")

    # plotting the lemma accs
    plt.plot(possible_steps, dev_lemma_accs, "-o", label="dev lemma acc")

    plt.plot(possible_steps, train_form_accs, "-o", label="train form acc")

    # plotting the lemma accs
    plt.plot(possible_steps, train_lemma_accs, "-o", label="train lemma acc")

    # naming the x axis
    plt.xlabel("Training steps")
    # naming the y axis
    plt.ylabel("Acc")
    # giving a title to my graph
    plt.title(f"{args.name}: train & dev acc during training")

    # show a legend on the plot
    plt.legend()

    plt.grid()

    plt.savefig(filename)

    # Clear the plot
    plt.clf()


if __name__ == "__main__":
    args = parser.parse_args([] if "__file__" not in globals() else None)
    main(args)
