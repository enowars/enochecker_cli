import argparse
import json

from enochecker_cli import add_arguments, json_task_message_from_namespace


def test_json_checker_message():
    argv = [
        "putflag",
        "-i",
        "17",
        "-a",
        "example",
        "-T",
        "19",
        "-t",
        "TestTeam",
        "-r",
        "3",
        "-R",
        "2",
        "-f",
        "ENOTESTFLAG",
        "-v",
        "4",
        "-x",
        "15000",
        "-l",
        "50000",
    ]

    parser = argparse.ArgumentParser(description="Your friendly checker script")
    add_arguments(parser)

    ns = parser.parse_args(argv)
    msg = json.loads(json_task_message_from_namespace(ns))
    for key, val in {
        "taskId": 17,
        "method": "putflag",
        "address": "example",
        "teamId": 19,
        "teamName": "TestTeam",
        "currentRoundId": 3,
        "relatedRoundId": 2,
        "flag": "ENOTESTFLAG",
        "variantId": 4,
        "timeout": 15000,
        "roundLength": 50000,
        "taskChainId": "flag_s0_r2_t19_i4",
    }.items():
        assert key in msg
        assert msg[key] == val


def test_json_checker_message_no_flag():
    argv = ["havoc", "-i", "18", "-a", "example", "-T", "20", "-t", "TestTeam", "-r", "4", "-R", "3", "-v", "5", "-x", "16000", "-l", "51000"]

    parser = argparse.ArgumentParser(description="Your friendly checker script")
    add_arguments(parser)

    ns = parser.parse_args(argv)
    msg = json.loads(json_task_message_from_namespace(ns))
    for key, val in {
        "taskId": 18,
        "method": "havoc",
        "address": "example",
        "teamId": 20,
        "teamName": "TestTeam",
        "currentRoundId": 4,
        "relatedRoundId": 3,
        "variantId": 5,
        "timeout": 16000,
        "roundLength": 51000,
        "taskChainId": "havoc_s0_r3_t20_i5",
    }.items():
        assert key in msg
        assert msg[key] == val
