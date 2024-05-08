"""Read an excel file with times downloaded from TimeEdit and sort the data
per person. Then sum up the times for every person in courses and categories."""
from collections import defaultdict
import pathlib
import pickle
import pandas
import numpy
import staffing.staffing as staffing


FRAME_FILE = pathlib.Path("data/personal_frames.pkl")
LISTS_FILE = pathlib.Path("data/personal_lists.pkl")


class ExcelWriter:
    """A class used for writing personal dataframes to a larger excel file"""
    def __init__(self, file_name) -> None:
        self.writer = pandas.ExcelWriter(file_name, engine='openpyxl')
        self.startrow = defaultdict(int)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.writer.close()

    def save(self):
        """Save the excel file"""
        self.writer.close()

    def write_person_frame(self, person, frame):
        """Write the personal frame to the excel file"""
        program = person.program
        # Write name and employment
        pandas.DataFrame([person.name, person.employment]).T.to_excel(
            self.writer, sheet_name=program,
            startrow=self.startrow[program],
            index=False, header=False)
        self.startrow[program] += 1

        # Write the dataframe
        frame.to_excel(self.writer, sheet_name=program,
                       startrow=self.startrow[program],
                       index=True, header=True)
        self.startrow[program] += len(frame) + 2

    def write_person_list(self, person, frame):
        """Write the personal frame to the excel file"""
        # Write name and employment
        pandas.DataFrame([person.name, person.employment]).T.to_excel(
            self.writer, sheet_name=person.name,
            startrow=0,
            index=False, header=False)

        # Write the dataframe
        frame.to_excel(self.writer, sheet_name=person.name,
                       startrow=2,
                       index=True, header=True)


def main():
    """Do the thing"""
    with open(FRAME_FILE, "rb") as file:
        personal_frames = pickle.load(file)
    with open(LISTS_FILE, "rb") as file:
        personal_lists = pickle.load(file)

    programs = list(numpy.unique([p.program for p in personal_frames.keys()]))
    # programs = ["molekylar-biofysik"]

    for program in programs:
        output_file = f"results/Bemanning2023_{program}.xlsx"
        people_in_program = [p for p in personal_frames.keys()
                             if p.program == program]

        with ExcelWriter(output_file) as writer:
            for person in people_in_program:
                this_frame = personal_frames[person]
                if this_frame is not None:
                    writer.write_person_frame(person, this_frame)
                this_list = personal_lists[person]
                if this_list is not None:
                    writer.write_person_list(person, this_list)

        staffing.make_columns_larger(output_file)

if __name__ == "__main__":
    main()
