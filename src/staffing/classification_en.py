from enum import Enum


class Events(Enum):
    LECTURE = "Lecture"
    LABORATORY = "Laboratory"
    EXCURSION = "Excursion"
    SEMINAR = "Seminar"
    UNKNOWN = "Unknown"


EVENT_TYPES = {
    Events.LECTURE: ["Lecture", "Lesson", "Presentation", "Demonstration",
                     "Introduction", "Information"],
    Events.LABORATORY: ["Laboratory", "Lab"],
    Events.EXCURSION: ["Study visit"],
    Events.SEMINAR: ["Seminar", "Question time", "Meeting", "Symposium",
                     "Case", "Workshop", "Conference", "Project"]
}

CATEGORY_NAMES = {
    Events.LECTURE: "Lecture",
    Events.LABORATORY: "Laboratory",
    Events.EXCURSION: "Excursion",
    Events.SEMINAR: "Seminar",
    Events.UNKNOWN: "Unknown",
}

# array([nan, 'Compulsory, Seminar', 'Question time', 'Meeting',
#        'Question time, Utvärdering', 'CANCELLED, Study visit',
#        'Seminar, lecture via Zoom', 'Exam', 'Lecture', 'Lesson',
#        'Presentation', 'Laboratory experiment',
#        'CANCELLED, Compulsory, Demonstration', 'Seminar', 'Symposium',
#        'Research', 'Exam, E-exam', 'Compulsory, Presentation, Seminar',
#        'Compulsory, Presentation, lecture via Zoom',
#        'Compulsory, Presentation', 'Videoconference', 'Introduction',
#        'Online lecture', 'Introduction, Lecture, lecture via Zoom',
#        'Compulsory, Case', 'Information, lecture via Zoom',
#        'Compulsory, Introduction, lecture via Zoom',
#        'Compulsory, Introduction, Lecture, lecture via Zoom',
#        'Computer lab, lecture via Zoom', 'Lecture, lecture via Zoom',
#        'Compulsory, Lecture',
#        'Compulsory, Introduction, Laboratory experiment, lecture via Zoom',
#        'Workshop', 'Lecture, Recorded lecture', 'Compulsory, Workshop',
#        'Computer lab', 'Meeting, Kalendarium EDU', 'Problemlösning',
#        'Presentation, lecture via Zoom',
#        'Question time, lecture via Zoom',
#        'Compulsory, Laboratory experiment, Seminar',
#        'Compulsory, Laboratory experiment', 'Compulsory',
#        'Project, Presentation', 'Compulsory, Introduction, Roll-call',
#        'Recorded lecture', 'Other',
#        'Compulsory, Computer lab, lecture via Zoom',
#        'Introduction, Lecture',
#        'Meeting, Videoconference, Kalendarium EDU',
#        'Compulsory, Question time', 'Forskarseminarium',
#        'Compulsory, Information', 'Information, Meeting via Zoom',
#        'Course', 'Roll-call',
#        'Compulsory, Introduction, Laboratory experiment',
#        'Compulsory, Lesson', 'Study visit',
#        'Laboratory experiment, Presentation', 'Compulsory, Computer lab',
#        'SI-Meeting', 'Under construction', 'Project',
#        'Postgraduate course', 'Compulsory, Lecture, Roll-call',
#        'Compulsory, Exercise', 'Laboratory experiment, Seminar',
#        'preparation', 'Compulsory, Hand-in, Laboratory experiment',
#        'Lunch', 'Lokalbokning',
#        'Lecture, Question time, lecture via Zoom',
#        'Degree project presentation', 'Thesis defence', 'Studentactivity',
#        'Other, Kalendarium EDU', 'Compulsory, Roll-call',
#        'Compulsory, Introduction, Lecture', 'Information',
#        'Compulsory, Professional Training', 'Compulsory, Introduction',
#        'Compulsory, Simulering', 'Laboratory experiment, preparation',
#        'Tutorials', 'Exercise', 'Compulsory, Group work', 'Group work',
#        'Conference', 'Test', 'Compulsory, Other, Seminar',
#        'Compulsory, Study visit',
#        'Compulsory, Introduction, Laboratory experiment, Lecture',
#        'Simulering', 'Tutorials, lecture via Zoom',
#        'Thesis defence, Mottagning', 'Compulsory, Diskussion',
#        'Compulsory, Examination',
#        'Compulsory, Laboratory experiment, Supervision', 'Diskussion',
#        'Question time, Kursvärdering', 'Compulsory, Exam, E-exam',
#        'Supervision', 'Compulsory, Lecture, Presentation',
#        'Compulsory, Project, Review', 'Compulsory, Computer lab, Lecture',
#        'Self-study', 'Diagnostic test', 'Theory lab',
#        'Compulsory, Demonstration', 'CANCELLED',
#        'Introduction, Laboratory experiment',
#        'Compulsory, Demonstration, Reserv',
#        'Supervision, lecture via Zoom', 'Muddy Points',
#        'Compulsory, Exam', 'Compulsory, Minisymposium'], dtype=object)