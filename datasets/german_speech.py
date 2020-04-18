"""German speech dataset using https://github.com/german-asr/megs"""
__author__ = 'Erdene-Ochir Tuguldur'

import os
import csv

import numpy as np
from torch.utils.data import Dataset


vocab = "B abcdefghijklmnopqrstuvwxyzäöü"  # B: blank
char2idx = {char: idx for idx, char in enumerate(vocab)}
idx2char = {idx: char for idx, char in enumerate(vocab)}


def convert_text(text):
    return [char2idx[char] for char in text if char != 'B']


def read_metadata(dataset_path, metadata_file, max_duration):
    fnames, texts = [], []

    reader = csv.reader(open(metadata_file, 'rt'))
    for line in reader:
        fname, duration, text = line[0], line[1], line[2]
        try:
            duration = float(duration)
            if duration > max_duration:
                continue
        except ValueError:
            continue
        fnames.append(os.path.join(dataset_path, fname))
        texts.append(np.array(convert_text(text)))

    return fnames, texts


class GermanSpeech(Dataset):

    def __init__(self, name='train', max_duration=16.7, transform=None):
        self.transform = transform

        datasets_path = os.path.dirname(os.path.realpath(__file__))
        dataset_path = os.path.join(datasets_path, 'GermanSpeech')
        csv_file = os.path.join(dataset_path, 'megs-%s.csv' % name)
        self.fnames, self.texts = read_metadata(dataset_path, csv_file, max_duration)

    def __getitem__(self, index):
        data = {
            'fname': self.fnames[index],
            'text': self.texts[index]
        }

        if self.transform is not None:
            data = self.transform(data)

        return data

    def __len__(self):
        return len(self.fnames)
