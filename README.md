# wizcli

![test](https://github.com/redraw/wizcli/actions/workflows/test.yml/badge.svg)

Control your WiZ light from the CLI.

## Install

```bash
pip install wizcli
```
## Use

```bash
# turn on
wiz on

# turn off
wiz off

# dim to 20%
wiz dim 20

# set temp to 50%
wiz temp 50

# set cold
wiz cold

# set warm
wiz warm

# set RGB color
wiz rgb 255 40 90
```

## Help
```bash
Usage: wiz [OPTIONS] COMMAND [ARGS]...

Options:
  -h, --host TEXT                 WiZ bulb host  [env var: WIZ_HOST]
  -p, --port INTEGER              WiZ bulb port  [env var: WIZ_PORT; default:
                                  38899]
  -t, --timeout INTEGER           Timeout in seconds  [env var: WIZ_TIMEOUT;
                                  default: 5]
  -v, --verbose
  --help                          Show this message and exit.

Commands:
  cold
  dim
  get
  off
  on
  rgb
  switch
  temp
  warm

```
