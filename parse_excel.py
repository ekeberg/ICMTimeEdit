"""Read an excel file with times downloaded from TimeEdit and sort the data
per person. Then sum up the times for every person in courses and categories."""
import pathlib
import warnings
import pickle
import pandas
import staffing


def main():
    """Do the thing"""
    # Read people data
    with open("data/people_per_program.pkl", "rb") as file:
        people = pickle.load(file)

    excel_path = pathlib.Path('data/TimeEdit2023.xlsx')
    data = pandas.read_excel(excel_path, header=5, index_col=0)

    # Remove rows with no person or course name such, as holidays
    data = data.dropna(subset=["Personal", "Kurssignatur"])

    personal_frames = {}
    personal_lists = {}

    for person in people:
        mask = data["Personal"].str.contains(person.name)
        my_data = data[mask]

        if my_data.empty:
            personal_frames[person] = None
            personal_lists[person] = None
            continue

        print(person.name, len(my_data))

        person_table = build_personal_frame(person, my_data)
        personal_frames[person] = person_table

        person_list = buld_personal_list_of_events(person, my_data)
        personal_lists[person] = person_list

    with open("data/personal_frames.pkl", "wb") as file:
        pickle.dump(personal_frames, file)

    with open("data/personal_lists.pkl", "wb") as file:
        pickle.dump(personal_lists, file)


class EventTypeWarning(Warning):
    """Raised when an event type is not recognized"""


def identify_event_type(event):
    """Identify the type of event"""

    moment = event["Moment"]

    for key, value in staffing.EVENT_TYPES.items():
        for v in value:
            if v.lower() in moment.lower():
                return key

    warnings.warn(f"Could not find event type for {moment}",
                  EventTypeWarning)
    return "Okänd"


def build_personal_frame(person, data):
    """Build a frame with the summary of a persons teaching broken down per
    course and type of teaching for a person"""
    columns = tuple(staffing.EVENT_TYPES.keys()) + ("Okänd",)
    person_table = pandas.DataFrame(0., index=data["Kurssignatur"].unique(),
                                    columns=columns)

    # Add course names
    unique_courses_df = data.drop_duplicates(subset=["Kurssignatur", "Kurs"])
    course_mapping = dict(zip(unique_courses_df["Kurssignatur"],
                              unique_courses_df["Kurs"]))
    person_table.insert(0, "Kursnamn", "")
    for signatur, kurs in course_mapping.items():
        person_table.at[signatur, "Kursnamn"] = kurs

    # Loop over all teaching events and categorize them
    for _, event in data.iterrows():
        minutes = staffing.time_diff(event["Starttid"], event["Sluttid"])
        hours = staffing.minutes_to_lecture_hours(minutes)

        event_type = identify_event_type(event)
        person_table.at[event["Kurssignatur"], event_type] += hours


    # Add a column with the total weighted number of hours
    my_factors = staffing.get_factors_for_person(person)

    summary_column = 0
    for event_type in columns:
        summary_column += person_table[event_type] * my_factors[event_type]
    person_table["Totalt"] = summary_column

    # Add sum row at the bottom
    summary_row = person_table.sum()
    summary_row["Kursnamn"] = "Totalt"
    person_table = pandas.concat(
        [person_table, summary_row.to_frame().T])

    return person_table


def buld_personal_list_of_events(person, data):
    """Build a frame with the a list of all events for a person"""
    columns = ["Kursnamn", "Kurskod", "Moment", "Datum", "Starttid",
               "Sluttid", "Timmar", "Kategori", "Timmar (justerade)"]
    person_table = pandas.DataFrame(columns=columns, index=None)

    counter = 0
    for _, event in data.iterrows():
        minutes = staffing.time_diff(event["Starttid"], event["Sluttid"])
        hours = staffing.minutes_to_lecture_hours(minutes)

        event_type = identify_event_type(event)

        my_factors = staffing.get_factors_for_person(person)
        adjusted_hours = hours * my_factors[event_type]

        values = [event["Kurs"], event["Kurssignatur"], event["Moment"],
                  event["Startdatum"], event["Starttid"],
                  event["Sluttid"], hours, event_type,
                  adjusted_hours]
        row = dict(zip(columns, values))

        person_table.loc[counter] = row
        counter += 1

    return person_table


if __name__ == "__main__":
    main()
