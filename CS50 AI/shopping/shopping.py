from asyncore import read
from calendar import month
import csv
from optparse import Values
import sys
import datetime

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4

def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    
    evidence = list()
    labels = list()

    # read the file
    with open(filename) as file:
        data = csv.DictReader(file)

        for values in data:
            # evidence
            evidence.append([
                int(values["Administrative"]), # Administrative
                float(values["Administrative_Duration"]), # Administrative_Duration
                int(values["Informational"]), # Informational
                float(values["Informational_Duration"]), # Informational_Duration
                int(values["ProductRelated"]), # ProductRelated
                float(values["ProductRelated_Duration"]), # ProductRelated_Duration
                float(values["BounceRates"]), # BounceRates
                float(values["ExitRates"]), # ExitRates
                float(values["PageValues"]), # PageValues
                float(values['SpecialDay']), # SpecialDay
                int(month_converter(values["Month"])), # Month
                int(values["OperatingSystems"]), # OperatingSystems
                int(values["Browser"]), # Browser
                int(values["Region"]), # Region
                int(values["TrafficType"]), # TrafficType
                int(converter(values["VisitorType"])), # VisitorType
                int(converter(values["Weekend"])), # Weekend
            ])

            # labels
            labels.append(
                int(converter("Revenue")) # Revenue
            )

    return (evidence, labels)       


def month_converter(month):
    """
    Function that converts month abbreviation to number
    """
    # months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    month_number = None

    # if month is june
    if month == "June":
        # convert it to jun
        month = "Jun"

    # convert month abbrv into number
    datetime_object = datetime.datetime.strptime(month, "%b")
    month_number = datetime_object.month

    return (month_number - 1)


def converter(value):
    """
    Convert value to 1 or 0 according to their value
    """
    number = 0

    # weekend and revenue
    # TRUE / FALSE
    if value == "FALSE":
        number = 0

    elif value == "TRUE":
        number = 1

    # visitor type
    if value == "Returning_Visitor":
        number = 1
    
    # new visitor
    elif value == "New_Visitor":
        number = 0

    return number  


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence, labels)
    return model

def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    positive = 0
    negative = 0
    positive_total = labels.count(1)
    negative_total = labels.count(0)

    for actual, predicted in zip(labels, predictions):
        # if actual and predicted are the same
        if actual == predicted:
            # didnt go through with purchase
            if predicted == 0:
                negative += 1
            
            # went through with purchase
            elif predicted == 1:
                positive += 1
    
    # print(f"{positive}, {negative}")
    # print(f"{positive_total}, {negative_total}")
    sensitivity = positive / positive_total
    specificity = negative / negative_total

    return (sensitivity, specificity)

if __name__ == "__main__":
    main()
