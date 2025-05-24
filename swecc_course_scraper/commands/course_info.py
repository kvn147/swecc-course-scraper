import json
import re
from typing import Any, Dict, List, Optional

import requests
from bs4 import BeautifulSoup

CATALOG_URL = "https://www.washington.edu/students/crscat/"

def fetch_html(url: str) -> str:
    """
    Fetches the HTML content of the given UW time schedule webpage.

    Args:
        url (str): The URL of the webpage.

    Returns:
        str: The raw HTML content of the webpage.

    Raises:
        FileNotFoundError: If the page does not exist (404).
        ConnectionError: If there is a network issue.
    """
    try:
        res = requests.get(url)
        res.raise_for_status()
        return res.text
    except requests.exceptions.HTTPError as e:
        raise FileNotFoundError(f"Page not found or no courses available: \n{e}") from e
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"Unable to connect to {url}: \n{e}") from e

def parse_course_info(html: str) -> Dict[str, Any]:

    course_info =  {
        "course_code": "",
        "title": "",
        "credits": None,
        "gen_ed": [],
        "description": "",
        "prerequisites": "",
    }

def command(course_code: str) -> str:

    course_department = "".join(filter(str.isalpha, course_code)).lower()
    course_number = "".join(filter(str.isdigit, course_code))
    course_code = f"{course_department}{course_number}"

    try:
        course_code_url = f"{CATALOG_URL}{course_department}/{course_code}.html"

        if not course_code_url:
            raise ValueError(f"Course {course_code} not found in the catalog.")

        return json.dumps(parse_course_info(fetch_html(course_code_url)), indent=4)

    except ConnectionError as e:
        return f"Connection error while fetching course information for {course_code}: {e}"
    except (FileNotFoundError, ConnectionError) as e:
        return f"Error fetching course information for {course_code}: {e}"
