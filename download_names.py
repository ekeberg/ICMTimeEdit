"""Download employee data from the research programs of ICM. Save this data
to file"""
import re
import pickle
from typing import Tuple
import requests
from bs4 import BeautifulSoup
import staffing


SAVE = True
PROGRAMS = ["bbbi",
            "mikrobiologi-immunologi",
            "molekylarbiologi",
            "molekylar-biofysik",
            "molekylar-evolution",
            "molekylar-systembiologi",
            "strukturbiologi"]


class LineParsingError(Exception):
    """Raised when a line cannot be parsed"""



def parse_line(line: str) -> Tuple[str, str, str]:
    """Parse a line of text"""
    pattern = r"\t\n(.+?), (.+?) \n+(.+?)\n"
    m = re.search(pattern, line)
    if m:
        last_name = m.group(1)
        first_name = m.group(2)
        employment = m.group(3)
        return first_name, last_name, employment
    else:
        raise LineParsingError(f"Could not parse line: {line}")


def main():
    """Download employee data from the research programs of ICM. Save
    this data"""
    people = []

    failed_people = []

    for program in PROGRAMS:
        url = f"https://www.icm.uu.se/{program}/om-oss"
        print(url)

        # Download the page
        response = requests.get(url, timeout=20)
        soup = BeautifulSoup(response.text, "html.parser")
        lines = [li.get_text() for li in soup.find_all('li') if li.get_text().lstrip(" ") != '']

        # Parse the page
        for i, l in enumerate(lines):
            try:
                first_name, last_name, employment = parse_line(l)
                p = staffing.Person(first_name, last_name, employment, program)
                people.append(p)
            except LineParsingError:
                if i > 12:
                    # This is not part of the header, but still failed
                    failed_people.append((program, l))

    # Save program_people using pickle
    if SAVE:
        with open('data/people_per_program.pkl', 'wb') as file:
            pickle.dump(people, file)

    if failed_people:
        print("Failed to parse the following entries:")
        for p in failed_people:
            print(f"{p[0]}: {p[1]}")


if __name__ == "__main__":
    main()
