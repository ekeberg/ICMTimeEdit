import pandas
import staffing.staffing as staffing
import staffing.input_keys_en as input_keys
import staffing.output_keys_en as output_keys
import staffing.classification_en as classification

def build_summary_frame(person, data):
    """Build a frame with the summary of a persons teaching broken down per
    course and type of teaching for a person"""
    columns = tuple(classification.CATEGORY_NAMES.values())
    person_table = pandas.DataFrame(0., index=data[input_keys.SIGNATURE].unique(),
                                    columns=columns)

    # Add course names
    unique_courses_df = data.drop_duplicates(subset=[input_keys.SIGNATURE,
                                                     input_keys.COURSE_NAME])
    course_mapping = dict(zip(unique_courses_df[input_keys.SIGNATURE],
                              unique_courses_df[input_keys.COURSE_NAME]))
    person_table.insert(0, input_keys.COURSE_NAME, "")
    for signatur, kurs in course_mapping.items():
        person_table.at[signatur, input_keys.COURSE_NAME] = kurs

    # Loop over all teaching events and categorize them
    for _, event in data.iterrows():
        minutes = staffing.time_diff(event[input_keys.START_TIME],
                                     event[input_keys.END_TIME])
        hours = staffing.minutes_to_lecture_hours(minutes)

        event_type = staffing.identify_event_type(event[input_keys.TYPE])
        person_table.at[event[input_keys.SIGNATURE], classification.CATEGORY_NAMES[event_type]] += hours


    # Add a column with the total weighted number of hours
    my_factors = staffing.get_factors_for_person(person)

    summary_column = 0
    # for event_type in columns:
    for event_type in classification.Events:
        summary_column += (
            person_table[classification.CATEGORY_NAMES[event_type]] *
            my_factors[event_type])
    person_table[output_keys.TOTAL] = summary_column

    # Add sum row at the bottom
    summary_row = person_table.sum()
    summary_row[input_keys.COURSE_NAME] = output_keys.TOTAL
    person_table = pandas.concat(
        [person_table, summary_row.to_frame().T])

    return person_table


def build_list_of_events(person, data):
    """Build a frame with the a list of all events for a person"""
    columns = [output_keys.COURSE_NAME, output_keys.COURSE_CODE,
               output_keys.TYPE, output_keys.DATE,
               output_keys.START_TIME, output_keys.END_TIME,
               output_keys.HOURS, output_keys.CLASSIFICATION,
               output_keys.ADJUSTED_HOURS]
    person_table = pandas.DataFrame(columns=columns, index=None)

    counter = 0
    for _, event in data.iterrows():
        minutes = staffing.time_diff(event[input_keys.START_TIME],
                                     event[input_keys.END_TIME])
        hours = staffing.minutes_to_lecture_hours(minutes)

        event_type = staffing.identify_event_type(event[input_keys.TYPE])

        my_factors = staffing.get_factors_for_person(person)
        adjusted_hours = hours * my_factors[event_type]

        values = [event[input_keys.COURSE_NAME],
                  event[input_keys.SIGNATURE],
                  event[input_keys.TYPE],
                  event[input_keys.DATE],
                  event[input_keys.START_TIME],
                  event[input_keys.END_TIME],
                  hours,
                  event_type,
                  adjusted_hours]
        row = dict(zip(columns, values))

        person_table.loc[counter] = row
        counter += 1

    return person_table
