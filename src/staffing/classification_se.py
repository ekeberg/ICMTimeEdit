from enum import Enum

class Events(Enum):
    LECTURE = "Föreläsning"
    LABORATORY = "Laboration"
    EXCURSION = "Exkursion"
    SEMINAR = "Seminarium"
    OTHER = "Övrigt"



EVENT_TYPES = {
    Events.LECTURE: ["Föreläsning", "Introduktion", "Upprop"],
    Events.LABORATORY: ["Laboration", "Datorlab", "Tutorials"],
    Events.EXCURSION: ["Studiebesök"],
    Events.SEMINAR: ["Seminarium", "Frågestund", "Presentation", "Fall",
                     "Lektion", "Övning", "Workshop", "Diskussion", "Case",
                     "Räkneövning", "Grupparbete", "Symposium", "Projekt",
                     "Problemlösning", "Redovisning"],
}
