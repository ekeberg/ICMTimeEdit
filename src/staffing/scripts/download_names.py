"""Download employee data from the research programs of ICM. Save this data
to file"""
import argparse
import pickle
from staffing import staffing
from staffing import teachers


def main():
    """Download employee data from the research programs of ICM. Save
    this data"""

    parser = argparse.ArgumentParser(
        description=("Download employee data from the research "
                     "programs of ICM. Save this data"))
    parser.add_argument("outfile",
                        help="Save the data here, as a python pickle file.")
    args = parser.parse_args()

    people = []

    for program in staffing.PROGRAMS:
        people += teachers.download_names(program)

    # Save program_people using pickle
    with open(args.outfile, 'wb') as file:
        pickle.dump(people, file)
