import argparse
import sys

import jsons
import requests
from enochecker_core import CheckerMethod, CheckerResultMessage, CheckerTaskMessage

TASK_TYPES = [str(i) for i in CheckerMethod]


def get_parser() -> argparse.ArgumentParser:
    return _get_parser(hide_checker_address=True)


def _get_parser(hide_checker_address=False) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Your friendly checker script")
    parser.add_argument("method", choices=TASK_TYPES, help="One of {} ".format(TASK_TYPES))
    if not hide_checker_address:
        parser.add_argument("-A", "--checker_address", type=str, default="http://localhost", help="The URL of the checker")
    parser.add_argument("-i", "--task_id", type=int, default=1, help="An id for this task. Must be unique in a CTF.")
    parser.add_argument("-a", "--address", type=str, default="localhost", help="The ip or address of the remote team to check")
    parser.add_argument("-T", "--team_id", type=int, default=1, help="The Team_id belonging to the specified Team")
    parser.add_argument("-t", "--team_name", type=str, default="team1", help="The name of the target team to check")
    parser.add_argument("-r", "--current_round_id", type=int, default=1, help="The round we are in right now")
    parser.add_argument(
        "-R",
        "--related_round_id",
        type=int,
        default=1,
        help="The round in which the flag or noise was stored when method is getflag/getnoise. Equal to current_round_id otherwise.",
    )
    parser.add_argument("-f", "--flag", type=str, default="ENOFLAGENOFLAG=", help="The Flag, a Fake flag or a Unique ID, depending on the mode")
    parser.add_argument("-v", "--variant_id", type=int, default=0, help="The variantId for the method being called")
    parser.add_argument(
        "-x", "--timeout", type=int, default=30000, help="The maximum amount of time the script has to execute in milliseconds (default 30 000)"
    )
    parser.add_argument("-l", "--round_length", type=int, default=300000, help="The round length in milliseconds (default 300 000)")
    parser.add_argument(
        "-I",
        "--task_chain_id",
        type=str,
        default=None,
        help="A unique Id which must be identical for all related putflag/getflag calls and putnoise/getnoise calls",
    )

    return parser


def task_message_from_namespace(ns: argparse.Namespace) -> CheckerTaskMessage:
    task_chain_id = ns.task_chain_id
    method = CheckerMethod(ns.method)
    if not task_chain_id:
        option = None
        if method in (CheckerMethod.CHECKER_METHOD_PUTFLAG, CheckerMethod.CHECKER_METHOD_GETFLAG):
            option = "flag"
        elif method in (CheckerMethod.CHECKER_METHOD_PUTNOISE, CheckerMethod.CHECKER_METHOD_GETNOISE):
            option = "noise"
        elif method == CheckerMethod.CHECKER_METHOD_HAVOC:
            option = "havoc"
        else:
            raise ValueError(f"Unexpected CheckerMethod: {method}")
        task_chain_id = f"{option}_s0_r{ns.related_round_id}_t{ns.team_id}_i{ns.variant_id}"

    msg = CheckerTaskMessage(
        task_id=ns.task_id,
        method=method,
        address=ns.address,
        team_id=ns.team_id,
        team_name=ns.team_name,
        current_round_id=ns.current_round_id,
        related_round_id=ns.related_round_id,
        flag=ns.flag,
        variant_id=ns.variant_id,
        timeout=ns.timeout,
        round_length=ns.round_length,
        task_chain_id=task_chain_id,
    )

    return msg


def json_task_message_from_namespace(ns: argparse.Namespace) -> str:
    return jsons.dumps(task_message_from_namespace(ns), use_enum_name=False, key_transformer=jsons.KEY_TRANSFORMER_CAMELCASE, strict=True)


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
