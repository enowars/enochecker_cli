import argparse
import sys

import jsons
import requests
from enochecker_core import CheckerResultMessage, CheckerTaskMessage, CheckerTaskType

TASK_TYPES = [str(i) for i in CheckerTaskType]


def get_parser() -> argparse.ArgumentParser:
    return _get_parser(hide_checker_address=True)


def _get_parser(hide_checker_address=False) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Your friendly checker script")
    parser.add_argument("method", choices=TASK_TYPES, help="One of {} ".format(TASK_TYPES))
    if not hide_checker_address:
        parser.add_argument("-A", "--checker_address", type=str, default="http://localhost", help="The URL of the checker")
    parser.add_argument("-a", "--address", type=str, default="localhost", help="The ip or address of the remote team to check")
    parser.add_argument("-t", "--team_name", type=str, default="team1", help="The name of the target team to check")
    parser.add_argument("-T", "--team_id", type=int, default=1, help="The Team_id belonging to the specified Team")
    parser.add_argument("-I", "--run_id", type=int, default=1, help="An id for this run. Used to find it in the DB later.")
    parser.add_argument("-r", "--round_id", type=int, default=1, help="The round we are in right now")
    parser.add_argument("-R", "--round_length", type=int, default=300, help="The round length in seconds (default 300)")
    parser.add_argument("-f", "--flag", type=str, default="ENOFLAGENOFLAG=", help="The Flag, a Fake flag or a Unique ID, depending on the mode")
    parser.add_argument("-F", "--related_round_id", type=int, default=1, help="The Round the Flag belongs to (was placed)")
    parser.add_argument("-x", "--timeout", type=int, default=30, help="The maximum amount of time the script has to execute in seconds")
    parser.add_argument(
        "-i",
        "--flag_index",
        type=int,
        default=0,
        help="Unique numerical index per round. Each id occurs once and is tighly packed, "
        "starting with 0. In a service supporting multiple flags, this would be used to "
        "decide which flag to place.",
    )

    return parser


def task_message_from_namespace(ns: argparse.Namespace) -> CheckerTaskMessage:
    msg = CheckerTaskMessage(
        ns.run_id, ns.method, ns.address, 0, "", ns.team_id, ns.team_name, ns.round_id, ns.related_round_id, ns.flag, ns.flag_index,
    )  # service_id  # ns.service_name,

    return msg


def json_task_message_from_namespace(ns: argparse.Namespace) -> str:
    return jsons.dumps(task_message_from_namespace(ns), key_transformer=jsons.KEY_TRANSFORMER_CAMELCASE)


def main():
    ns = _get_parser().parse_args(sys.argv[1:])
    msg = json_task_message_from_namespace(ns)

    result = requests.post(ns.checker_address, data=msg, headers={"content-type": "application/json"},)
    if result.ok:
        result_msg = jsons.loads(result.content, CheckerResultMessage)
        print(result_msg.result)
    else:
        print(result.status_code)
        print(result.text)
