"""jc - JSON CLI output utility `uptime` command output parser

Usage (cli):

    $ uptime | jc --uptime

    or

    $ jc uptime

Usage (module):

    import jc.parsers.uptime
    result = jc.parsers.uptime.parse(uptime_command_output)

Compatibility:

    'linux', 'darwin', 'cygwin', 'aix', 'freebsd'

Example:

    $ uptime | jc --uptime -p
    {
      "time": "11:35",
      "uptime": "3 days, 4:03",
      "users": 5,
      "load_1m": 1.88,
      "load_5m": 2.0,
      "load_15m": 1.94,
      "time_hour": 11,
      "time_minute": 35,
      "time_second": null,
      "uptime_days": 3,
      "uptime_hours": 4,
      "uptime_minutes": 3,
      "uptime_total_seconds": 273780
    }

    $ uptime | jc --uptime -p -r
    {
      "time": "11:36",
      "uptime": "3 days, 4:04",
      "users": "5",
      "load_1m": "1.88",
      "load_5m": "1.99",
      "load_15m": "1.94"
    }
"""
import jc.utils


class info():
    version = '1.3'
    description = '`uptime` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux', 'darwin', 'cygwin', 'aix', 'freebsd']
    magic_commands = ['uptime']


__version__ = info.version


def process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (Dictionary) raw structured data to process

    Returns:

        Dictionary. Structured data with the following schema:

        {
          "time":                   string,
          "time_hour":              integer,
          "time_minute":            integer,
          "time_second":            integer,        # null if not displayed
          "uptime":                 string,
          "uptime_days":            integer,
          "uptime_hours":           integer,
          "uptime_minutes":         integer,
          "uptime_total_seconds":   integer,
          "users":                  integer,
          "load_1m":                float,
          "load_5m":                float,
          "load_15m":               float
        }
    """
    if 'time' in proc_data:
        time_list = proc_data['time'].split(':')
        proc_data['time_hour'] = int(time_list[0])
        proc_data['time_minute'] = int(time_list[1])
        if len(time_list) == 3:
            proc_data['time_second'] = int(time_list[2])
        else:
            proc_data['time_second'] = None

    # parse the uptime field. Here are the variations:
    # 0 min
    # 3 mins
    # 3 days,  2:54
    # 2 days, 19:32
    # 1 day, 29 min
    # 16:59
    if 'uptime' in proc_data:
        uptime_days = 0
        uptime_hours = 0
        uptime_minutes = 0
        uptime_total_seconds = 0

        if 'min' in proc_data['uptime']:
            uptime_minutes = int(proc_data['uptime'].split()[-2])

        if ':' in proc_data['uptime']:
            uptime_hours = int(proc_data['uptime'].split()[-1].split(':')[-2])
            uptime_minutes = int(proc_data['uptime'].split(':')[-1])

        if 'day' in proc_data['uptime']:
            uptime_days = int(proc_data['uptime'].split()[0])

        proc_data['uptime_days'] = uptime_days
        proc_data['uptime_hours'] = uptime_hours
        proc_data['uptime_minutes'] = uptime_minutes

        uptime_total_seconds = (uptime_days * 86400) + (uptime_hours * 3600) + (uptime_minutes * 60)
        proc_data['uptime_total_seconds'] = uptime_total_seconds

    # integer conversions
    int_list = ['users']
    for key in int_list:
        if key in proc_data:
            try:
                key_int = int(proc_data[key])
                proc_data[key] = key_int
            except (ValueError):
                proc_data[key] = None

    # float conversions
    float_list = ['load_1m', 'load_5m', 'load_15m']
    for key in float_list:
        if key in proc_data:
            try:
                key_float = float(proc_data[key])
                proc_data[key] = key_float
            except (ValueError):
                proc_data[key] = None

    return proc_data


def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) output preprocessed JSON if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        Dictionary. Raw or processed structured data
    """
    if not quiet:
        jc.utils.compatibility(__name__, info.compatible)

    raw_output = {}
    cleandata = data.splitlines()

    if jc.utils.has_data(data):
        time, _, *uptime, users, _, _, _, load_1m, load_5m, load_15m = cleandata[0].split()

        raw_output['time'] = time
        raw_output['uptime'] = ' '.join(uptime).rstrip(',')
        raw_output['users'] = users
        raw_output['load_1m'] = load_1m.rstrip(',')
        raw_output['load_5m'] = load_5m.rstrip(',')
        raw_output['load_15m'] = load_15m

    if raw:
        return raw_output
    else:
        return process(raw_output)
