import argparse
import hashlib
import sys

import jsons
import requests
from enochecker_core import CheckerMethod, CheckerResultMessage, CheckerTaskMessage

TASK_TYPES = [str(i) for i in CheckerMethod]


def add_arguments(parser: argparse.ArgumentParser) -> None:
    _add_arguments(parser, hide_checker_address=True)


def _add_arguments(parser: argparse.ArgumentParser, hide_checker_address=False) -> None:
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
    parser.add_argument("-f", "--flag", type=str, default="ENOFLAGENOFLAG=", help="The flag for putflag/getflag or the flag to find in exploit mode")
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
    parser.add_argument("--flag_regex", type=str, default=None, help="A regular expression matched by the flag, used only when running the exploit method")
    parser.add_argument(
        "--attack_info", type=str, default=None, help="The attack info returned by the corresponding putflag, used only when running the exploit method"
    )


def task_message_from_namespace(ns: argparse.Namespace) -> CheckerTaskMessage:
    task_chain_id = ns.task_chain_id
    method = CheckerMethod(ns.method)
    if not task_chain_id:
        option = None
        if method in (CheckerMethod.PUTFLAG, CheckerMethod.GETFLAG):
            option = "flag"
        elif method in (CheckerMethod.PUTNOISE, CheckerMethod.GETNOISE):
            option = "noise"
        elif method == CheckerMethod.HAVOC:
            option = "havoc"
        elif method == CheckerMethod.EXPLOIT:
            option = "exploit"
        else:
            raise ValueError(f"Unexpected CheckerMethod: {method}")
        task_chain_id = f"{option}_s0_r{ns.related_round_id}_t{ns.team_id}_i{ns.variant_id}"

    flag_hash = None
    if method == CheckerMethod.EXPLOIT:
        flag_hash = hashlib.sha256(ns.flag.encode()).hexdigest()

    msg = CheckerTaskMessage(
        task_id=ns.task_id,
        method=method,
        address=ns.address,
        team_id=ns.team_id,
        team_name=ns.team_name,
        current_round_id=ns.current_round_id,
        related_round_id=ns.related_round_id,
        flag=ns.flag if method != CheckerMethod.EXPLOIT else None,
        variant_id=ns.variant_id,
        timeout=ns.timeout,
        round_length=ns.round_length,
        task_chain_id=task_chain_id,
        flag_regex=ns.flag_regex,
        flag_hash=flag_hash,
        attack_info=ns.attack_info,
    )

    return msg


def json_task_message_from_namespace(ns: argparse.Namespace) -> str:
    return jsons.dumps(task_message_from_namespace(ns), use_enum_name=False, key_transformer=jsons.KEY_TRANSFORMER_CAMELCASE, strict=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Your friendly checker script")
    _add_arguments(parser)
    ns = parser.parse_args(sys.argv[1:])
    msg = json_task_message_from_namespace(ns)

    result = requests.post(ns.checker_address, data=msg, headers={"content-type": "application/json"},)
    if result.ok:
        result_msg = jsons.loads(result.content, CheckerResultMessage)
        print(result_msg.result)
    else:
        print(result.status_code)
        print(result.text)
