import json

from enochecker_cli import get_parser, json_task_message_from_namespace


def test_json_checker_message():
    argv = [
        "putflag",
        "-a",
        "localhost",
        "-t",
        "TestTeam",
        "-I",
        "1",
        "-f",
        "ENOTESTFLAG",
        "-x",
        "30",
        "-i",
        "0",
        "-R",
        "500",
        "-F",
        "299",
        "-T",
        "19",
    ]

    ns = get_parser().parse_args(argv)
    msg = json.loads(json_task_message_from_namespace(ns))
    for (key, val) in {
        "runId": 1,
        "method": "putflag",
        "address": "localhost",
        "serviceId": 0,
        "serviceName": "",
        "teamId": 19,
        "teamName": "TestTeam",
        "roundId": 1,
        "relatedRoundId": 299,
        "flag": "ENOTESTFLAG",
        "flagIndex": 0,
    }.items():
        assert key in msg
        assert msg[key] == val


def test_json_checker_message_no_flag():
    argv = [
        "havoc",
        "-a",
        "localhost",
        "-t",
        "TestTeam",
        "-I",
        "1",
        "-x",
        "30",
        "-i",
        "0",
        "-R",
        "500",
        "-F",
        "299",
        "-T",
        "19",
    ]

    ns = get_parser().parse_args(argv)
    msg = json.loads(json_task_message_from_namespace(ns))
    for (key, val) in {
        "runId": 1,
        "method": "havoc",
        "address": "localhost",
        "serviceId": 0,
        "serviceName": "",
        "teamId": 19,
        "teamName": "TestTeam",
        "roundId": 1,
        "relatedRoundId": 299,
        "flagIndex": 0,
    }.items():
        assert key in msg
        assert msg[key] == val
