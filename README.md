# Enochecker CLI [![PyPI version](https://badge.fury.io/py/enochecker-cli.svg)](https://pypi.org/project/enochecker-cli) [![Build Status](https://github.com/enowars/enochecker_cli/actions/workflows/pythonapp.yml/badge.svg?branch=main)](https://github.com/enowars/enochecker_cli/actions/workflows/pythonapp.yml) ![Lines of code](https://tokei.rs/b1/github/enowars/enochecker_cli)


## Usage
```
usage: enochecker_cli [-h] [-A CHECKER_ADDRESS] [-i TASK_ID] [-a ADDRESS] [-T TEAM_ID] [-t TEAM_NAME] [-r CURRENT_ROUND_ID] [-R RELATED_ROUND_ID] [-f FLAG] [-v VARIANT_ID] [-x TIMEOUT] [-l ROUND_LENGTH] [-I TASK_CHAIN_ID]
                      [--flag_regex FLAG_REGEX] [--attack_info ATTACK_INFO]
                      {putflag,getflag,putnoise,getnoise,havoc,exploit}

Your friendly checker script

positional arguments:
  {putflag,getflag,putnoise,getnoise,havoc,exploit}
                        One of ['putflag', 'getflag', 'putnoise', 'getnoise', 'havoc', 'exploit']

options:
  -h, --help            show this help message and exit
  -A CHECKER_ADDRESS, --checker_address CHECKER_ADDRESS
                        The URL of the checker
  -i TASK_ID, --task_id TASK_ID
                        An id for this task. Must be unique in a CTF.
  -a ADDRESS, --address ADDRESS
                        The ip or address of the remote team to check
  -T TEAM_ID, --team_id TEAM_ID
                        The Team_id belonging to the specified Team
  -t TEAM_NAME, --team_name TEAM_NAME
                        The name of the target team to check
  -r CURRENT_ROUND_ID, --current_round_id CURRENT_ROUND_ID
                        The round we are in right now
  -R RELATED_ROUND_ID, --related_round_id RELATED_ROUND_ID
                        The round in which the flag or noise was stored when method is getflag/getnoise. Equal to current_round_id otherwise.
  -f FLAG, --flag FLAG  The flag for putflag/getflag or the flag to find in exploit mode
  -v VARIANT_ID, --variant_id VARIANT_ID
                        The variantId for the method being called
  -x TIMEOUT, --timeout TIMEOUT
                        The maximum amount of time the script has to execute in milliseconds (default 30 000)
  -l ROUND_LENGTH, --round_length ROUND_LENGTH
                        The round length in milliseconds (default 300 000)
  -I TASK_CHAIN_ID, --task_chain_id TASK_CHAIN_ID
                        A unique Id which must be identical for all related putflag/getflag calls and putnoise/getnoise calls
  --flag_regex FLAG_REGEX
                        A regular expression matched by the flag, used only when running the exploit method
  --attack_info ATTACK_INFO
                        The attack info returned by the corresponding putflag, used only when running the exploit method
```

## Installation
`pip3 install enochecker_cli`
