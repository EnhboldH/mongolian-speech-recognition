"""Data loader for the BolorSpeech dataset."""
__author__ = 'Erdene-Ochir Tuguldur'

import os
import csv

import numpy as np
from torch.utils.data import Dataset

from .mb_speech import vocab, convert_text


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


class BolorSpeech(Dataset):

    def __init__(self, name='train', max_duration=16.7, transform=None):
        self.transform = transform

        datasets_path = os.path.dirname(os.path.realpath(__file__))
        dataset_path = os.path.join(datasets_path, 'BolorSpeech')
        csv_file = os.path.join(dataset_path, 'bolor-%s.csv' % name)
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




