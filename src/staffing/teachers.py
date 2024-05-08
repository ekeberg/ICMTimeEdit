import re
import pickle
from typing import Tuple
import requests
from bs4 import BeautifulSoup
import staffing.staffing as staffing


PROGRAMS = {"bbbi": "https://www.uu.se/kontakt-och-organisation/organisation?query=X62:14",
            "mikrobiologi-immunologi": "https://www.uu.se/kontakt-och-organisation/organisation?query=X62:1",
            "molekylarbiologi": "https://www.uu.se/kontakt-och-organisation/organisation?query=X62:3",
            "molekylar-biofysik": "https://www.uu.se/kontakt-och-organisation/organisation?query=X62:6",
            "molekylar-evolution": "https://www.uu.se/kontakt-och-organisation/organisation?query=X62:12",
            "molekylar-systembiologi": "https://www.uu.se/kontakt-och-organisation/organisation?query=X62:13",
            "strukturbiologi": "https://www.uu.se/kontakt-och-organisation/organisation?query=X62:16"}


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


def download_names(program: str) -> list:
    """Download employee data from the research programs of ICM. Save
    this data"""
    people = []

    failed_people = []


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
                warnings.warn(f"Failed to parse line: {l}")

    return people