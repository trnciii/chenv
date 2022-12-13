import os, argparse, json, pprint

def file():
	return os.path.join(os.path.expanduser('~'), 'chenv.json')

def load():
	filepath = file()
	if os.path.exists(filepath):
		with open(filepath) as f:
			return json.load(f)
	else:
		return {}

def save(table):
	with open(file(), 'w') as f:
		json.dump(table, f, indent=2)


def add(key, path):
	table = load()

	if key in table.keys():
		print(f'{k} already exists. choose different name')
	else:
		table[key] = path

	save(table)


def ls(keys=False):
	if keys:
		print(' '.join(load().keys()))
	else:
		pprint.pprint(load())


def setup():
	return '''
chenv(){
	. "$(chenv-core activator $1)"
}

_chenv_init_completion(){
  COMPREPLY=()
  _get_comp_words_by_ref "$@" cur prev words cword
}

_chenv(){
  local cur prev words cword split
  if declare -F _init_completion >/dev/null 2>&1; then
    _init_completion -n :/ || return
  else
    _chenv_init_completion -n :/ || return
  fi

	COMPREPLY=( $(compgen -W "$(chenv-core list --keys)" -- "$cur") )
}

complete -F _chenv chenv
'''


def main():
	parser = argparse.ArgumentParser()
	subparsers = parser.add_subparsers()

	p = subparsers.add_parser('activator')
	p.add_argument('env', type=str)
	p.set_defaults(handler=lambda args:print(f'{load()[args.env]}/bin/activate'))

	p = subparsers.add_parser('add')
	p.add_argument('key', type=str)
	p.add_argument('path', type=str)
	p.set_defaults(handler=lambda args:add(args.key, os.path.abspath(args.path)))

	p = subparsers.add_parser('list')
	p.add_argument('--keys', action='store_true')
	p.set_defaults(handler=lambda args:ls(args.keys))

	subparsers.add_parser('setup').set_defaults(handler=lambda _:print(setup()))

	subparsers.add_parser('file').set_defaults(handler=lambda _:print(file() if os.path.exists(file()) else 'not exit'))


	args = parser.parse_args()
	if hasattr(args, 'handler'):
		args.handler(args)
