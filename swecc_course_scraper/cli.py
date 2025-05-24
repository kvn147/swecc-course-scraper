import argparse

from swecc_course_scraper.commands.frequency import DEFAULT_YEARS_CHECK
from swecc_course_scraper.commands.frequency import command as frequency
from swecc_course_scraper.commands.login import command as login
from swecc_course_scraper.commands.schedule import command as schedule
from swecc_course_scraper.commands.course_info import command as course_info


def main(args: argparse.Namespace) -> None:
    try:
        if args.login:
            login(args)
        elif args.schedule:
            department, quarter, year = args.schedule
            print(schedule(department, quarter, year))
        elif args.frequency:
            course_code = args.frequency[0]
            check_years = (
                int(args.frequency[1])
                if len(args.frequency) > 1
                else DEFAULT_YEARS_CHECK
            )
            print(frequency(course_code, check_years))
        elif args.course_info:
            print(course_info(args.course_info))
        else:
            print("No command specified. Use --help to show all commands.")

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--login", action="store_true", help="Log in to DawgPath")
    parser.add_argument(
        "--schedule",
        nargs=3,
        metavar=("DEPARTMENT", "QUARTER", "YEAR"),
        type=str,
        help="Get previous quarters schedules. \n e.g.: --schedule cse [WIN|SPR|SUM|AUT] 2023",
    )
    parser.add_argument(
        "--frequency",
        nargs="+",
        metavar=("COURSE_CODE", "YEARS_CHECK"),
        type=str,
        help=(
            "Get the frequency a course is offered by quarter within a specified number of"
            " years from today. \n"
            "COURSE_CODE: Course code to check \n"
            f"YEARS_CHECK: Number of years to check from today (Default {DEFAULT_YEARS_CHECK}"
            " years) \n"
            "e.g.: --frequency CSE143 5"
        ),
    )
    parser.add_argument(
        "--course_info",
        metavar="COURSE_CODE",
        type=str,
        help="Get detailed course information (credits, general education requirements, "
        "description, and prerequisites) for a specific course code. \n "
        "COURSE_CODE: Course code to check \n"
        "e.g.: --course_info PHYS121",
    )
    main(parser.parse_args())
