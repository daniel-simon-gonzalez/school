# Daniel Gonzalez, FSU Mathematics PhD
# Colton Piper, FSU Mathematics PhD
# Applied Machine Learning Assignment 6

import re
import numpy as np

training_data = ["./data/gisette/gisette-train.data", "./data/dexter/dexter-train.csv", "./data/madelon/madelon-train.data"]
test_data = ["./data/gisette/gisette-valid.data", "./data/dexter/dexter-valid.csv", "./data/madelon/madelon-valid.data"]

training_labels = ["./data/gisette/gisette-train.labels", "./data/dexter/dexter-train.labels", "./data/madelon/madelon-train.labels"]
test_labels = ["./data/gisette/gisette-valid.labels", "./data/dexter/dexter-valid.labels", "./data/madelon/madelon-valid.labels"]

#MAIN DATA PROCESSING
for f_train_data, f_test_data, f_train_labels, f_test_labels in zip(training_data, test_data, training_labels, test_labels):
    with open(f_train_data) as train, open(f_test_data) as test, open(f_train_labels) as train_labels, open(f_test_labels) as test_labels:
        print("Processing: " + str(f_train_data.split("/")[-1]))
        data = []
        valid = []
        data_labels = []
        valid_labels = []

        #INPUT DATA
        for line in train:
            data.append([float(x) for x in re.split(r'[, ]', line.strip().strip("\n"))])
        for line in test:
            valid.append([float(x) for x in re.split(r'[, ]', line.strip().strip("\n"))])
        for line in train_labels:
            data_labels.append([float(x) for x in re.split(r'[ ]', line.strip().strip("\n"))])
        for line in test_labels:
            valid_labels.append([float(x) for x in re.split(r'[ ]', line.strip().strip("\n"))])

        data = np.asarray(data)
        valid = np.asarray(valid)
        data_labels = np.asarray(data_labels)
        valid_labels = np.asarray(valid_labels)

        data_labels = data_labels.reshape(data_labels.shape[0])
        valid_labels = valid_labels.reshape(valid_labels.shape[0])

        #NORMALIZE
        avg = np.mean(data, axis=0)
        std = np.std(data, axis=0)

        data = (data - avg)/std
        data = data[:, (np.isfinite(data)).any(axis=0)]

        valid = (valid - avg)/std
        valid = valid[:, (np.isfinite(valid)).any(axis=0)]

        #RELABEL
        data_labels[data_labels != 1] = -1
        valid_labels[valid_labels != 1] = -1

        #OUTPUT DATA
        print("\t Writing normalized training data...")
        np.save("./data-norm/" + f_train_data.split("/")[-2] + "/" + f_train_data.split("/")[-1], data)

        print("\t Writing normalized validation data...")
        np.save("./data-norm/" + f_test_data.split("/")[-2] + "/" + f_test_data.split("/")[-1], valid)

        print("\t Writing training labels...")
        np.save("./data-norm/" + f_train_labels.split("/")[-2] + "/" + f_train_labels.split("/")[-1], data_labels)

        print("\t Writing validation labels...")
        np.save("./data-norm/" + f_test_labels.split("/")[-2] + "/" + f_test_labels.split("/")[-1], valid_labels)
