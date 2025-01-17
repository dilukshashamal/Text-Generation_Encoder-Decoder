import os
import warnings

warnings.filterwarnings("ignore")
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

import time

import numpy as np
import tensorflow as tf

path_to_file = tf.keras.utils.get_file(
    "shakespeare.txt",
    "https://storage.googleapis.com/download.tensorflow.org/data/shakespeare.txt",
)

text = open(path_to_file, "rb").read().decode(encoding="utf-8")
print(f"Length of text: {len(text)} characters")

print(text[:250])

vocab = sorted(set(text))
print(f"{len(vocab)} unique characters")

example_texts = ["abcdefg", "xyz"]

chars = tf.strings.unicode_split(example_texts, input_encoding="UTF-8")
chars

ids_from_chars = tf.keras.layers.StringLookup(
    vocabulary=list(vocab), mask_token=None
)

ids = ids_from_chars(chars)
ids

chars_from_ids = tf.keras.layers.StringLookup(
    vocabulary=ids_from_chars.get_vocabulary(), invert=True, mask_token=None
)

chars = chars_from_ids(ids)
chars

tf.strings.reduce_join(chars, axis=-1).numpy()

def text_from_ids(ids):
    return tf.strings.reduce_join(chars_from_ids(ids), axis=-1)

all_ids = ids_from_chars(tf.strings.unicode_split(text, "UTF-8"))
all_ids

ids_dataset = tf.data.Dataset.from_tensor_slices(all_ids)

for ids in ids_dataset.take(10):
    print(chars_from_ids(ids).numpy().decode("utf-8"))

seq_length = 100
examples_per_epoch = len(text) // (seq_length + 1)

sequences = ids_dataset.batch(seq_length + 1, drop_remainder=True)

for seq in sequences.take(1):
    print(chars_from_ids(seq))

for seq in sequences.take(5):
    print(text_from_ids(seq).numpy())

def split_input_target(sequence):
    input_text = sequence[:-1]
    target_text = sequence[1:]
    return input_text, target_text

split_input_target(list("Tensorflow"))

dataset = sequences.map(split_input_target)

for input_example, target_example in dataset.take(1):
    print("Input :", text_from_ids(input_example).numpy())
    print("Target:", text_from_ids(target_example).numpy())

BATCH_SIZE = 64

BUFFER_SIZE = 10000

dataset = (
    dataset.shuffle(BUFFER_SIZE)
    .batch(BATCH_SIZE, drop_remainder=True)
    .prefetch(tf.data.experimental.AUTOTUNE)
)

dataset
