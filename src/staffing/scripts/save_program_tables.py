"""Read an excel file with times downloaded from TimeEdit and sort the data
per person. Then sum up the times for every person in courses and categories."""
import pathlib
import pickle
import argparse
import pandas
import staffing.staffing as staffing
import staffing.frames as frames
import staffing.write_excel as write_excel
import staffing.input_keys_en as input_keys

def main():
    parser = argparse.ArgumentParser(
        description=("Read an excel file with times downloaded from TimeEdit "
                     "and sort the data per person. Then sum up the times for "
                     "every person in courses and categories and output it to"
                     "excel files, sorted by research program."))
    parser.add_argument("people_file",
                        help=("The file with people data, generated "
                              "by icm_download_names"))
    parser.add_argument("teaching_file",
                        help=("The Excel file containing the teaching data, "
                              "downloaded from TimeEdit"))
    parser.add_argument("outdir",
                        help="Save the excel sheets here. One per program")
    parser.add_argument("--name", "-n",
                        help="This output file names will be this name plus "
                        "the program name.",
                        default=None)
    args = parser.parse_args()

    people_file = pathlib.Path(args.people_file)
    teaching_file = pathlib.Path(args.teaching_file)
    output_dir = pathlib.Path(args.outdir)
    if not output_dir.exists():
        output_dir.mkdir(parents=True)

    if not people_file.exists():
        raise FileNotFoundError(f"{people_file} does not exist")
    

    # Read people data
    with open(people_file, "rb") as file:
        people = pickle.load(file)

    data = pandas.read_excel(teaching_file, header=5, index_col=0)

    # Remove rows with no person or course name such, as holidays
    data = data.dropna(subset=[input_keys.STAFF, input_keys.SIGNATURE])

    summary_frames = {}
    event_lists = {}

    for person in people:
        mask = data[input_keys.STAFF].str.contains(person.name)
        my_data = data[mask]

        if my_data.empty:
            summary_frames[person] = None
            event_lists[person] = None
            continue

        print(person.name, len(my_data))

        person_table = frames.build_summary_frame(person, my_data)
        summary_frames[person] = person_table

        person_list = frames.build_list_of_events(person, my_data)
        event_lists[person] = person_list

    for program in staffing.PROGRAMS:
        output_name = f"{args.name}_" if args.name is not None else ""
        output_name += f"{program}.xlsx"
        output_file = output_dir / output_name
        people_in_program = [p for p in summary_frames
                             if p.program == program]

        with write_excel.ExcelWriter(output_file) as writer:
            for person in people_in_program:
                this_frame = summary_frames[person]
                if this_frame is not None:
                    writer.write_person_frame(person, this_frame)
                this_list = event_lists[person]
                if this_list is not None:
                    writer.write_person_list(person, this_list)

        write_excel.make_columns_larger(output_file)


if __name__ == "__main__":
    main()
