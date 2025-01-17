"""jc - JSON CLI output utility `rpm -qi` command output parser

Works with `rpm -qi [package]` or `rpm -qia`.

The `build_epoch` calculated timestamp field is naive (i.e. based on the local time of the system the parser is run on)

The `build_epoch_utc` calculated timestamp field is timezone-aware and is only available if the timezone field is UTC.

Usage (cli):

    $ rpm -qia | jc --rpm_qi

    or

    $ jc rpm -qia

Usage (module):

    import jc.parsers.rpm_qi
    result = jc.parsers.rpm_qi.parse(rpm_qi_command_output)

Compatibility:

    'linux'

Examples:

    $ rpm -qia | jc --rpm_qi -p
    [
      {
        "name": "make",
        "epoch": 1,
        "version": "3.82",
        "release": "24.el7",
        "architecture": "x86_64",
        "install_date": "Wed 16 Oct 2019 09:21:42 AM PDT",
        "group": "Development/Tools",
        "size": 1160660,
        "license": "GPLv2+",
        "signature": "RSA/SHA256, Thu 22 Aug 2019 02:34:59 PM PDT, Key ID 24c6a8a7f4a80eb5",
        "source_rpm": "make-3.82-24.el7.src.rpm",
        "build_date": "Thu 08 Aug 2019 05:47:25 PM PDT",
        "build_host": "x86-01.bsys.centos.org",
        "relocations": "(not relocatable)",
        "packager": "CentOS BuildSystem <http://bugs.centos.org>",
        "vendor": "CentOS",
        "url": "http://www.gnu.org/software/make/",
        "summary": "A GNU tool which simplifies the build process for users",
        "description": "A GNU tool for controlling the generation of executables and other non-source...",
        "build_epoch": 1565311645,
        "build_epoch_utc": null
      },
      {
        "name": "kbd-legacy",
        "version": "1.15.5",
        "release": "15.el7",
        "architecture": "noarch",
        "install_date": "Thu 15 Aug 2019 10:53:08 AM PDT",
        "group": "System Environment/Base",
        "size": 503608,
        "license": "GPLv2+",
        "signature": "RSA/SHA256, Mon 12 Nov 2018 07:17:49 AM PST, Key ID 24c6a8a7f4a80eb5",
        "source_rpm": "kbd-1.15.5-15.el7.src.rpm",
        "build_date": "Tue 30 Oct 2018 03:40:00 PM PDT",
        "build_host": "x86-01.bsys.centos.org",
        "relocations": "(not relocatable)",
        "packager": "CentOS BuildSystem <http://bugs.centos.org>",
        "vendor": "CentOS",
        "url": "http://ftp.altlinux.org/pub/people/legion/kbd",
        "summary": "Legacy data for kbd package",
        "description": "The kbd-legacy package contains original keymaps for kbd package. Please note...",
        "build_epoch": 1540939200,
        "build_epoch_utc": null
      },
      ...
    ]

    $ rpm -qia | jc --rpm_qi -p -r
    [
      {
        "name": "make",
        "epoch": "1",
        "version": "3.82",
        "release": "24.el7",
        "architecture": "x86_64",
        "install_date": "Wed 16 Oct 2019 09:21:42 AM PDT",
        "group": "Development/Tools",
        "size": "1160660",
        "license": "GPLv2+",
        "signature": "RSA/SHA256, Thu 22 Aug 2019 02:34:59 PM PDT, Key ID 24c6a8a7f4a80eb5",
        "source_rpm": "make-3.82-24.el7.src.rpm",
        "build_date": "Thu 08 Aug 2019 05:47:25 PM PDT",
        "build_host": "x86-01.bsys.centos.org",
        "relocations": "(not relocatable)",
        "packager": "CentOS BuildSystem <http://bugs.centos.org>",
        "vendor": "CentOS",
        "url": "http://www.gnu.org/software/make/",
        "summary": "A GNU tool which simplifies the build process for users",
        "description": "A GNU tool for controlling the generation of executables and other..."
      },
      {
        "name": "kbd-legacy",
        "version": "1.15.5",
        "release": "15.el7",
        "architecture": "noarch",
        "install_date": "Thu 15 Aug 2019 10:53:08 AM PDT",
        "group": "System Environment/Base",
        "size": "503608",
        "license": "GPLv2+",
        "signature": "RSA/SHA256, Mon 12 Nov 2018 07:17:49 AM PST, Key ID 24c6a8a7f4a80eb5",
        "source_rpm": "kbd-1.15.5-15.el7.src.rpm",
        "build_date": "Tue 30 Oct 2018 03:40:00 PM PDT",
        "build_host": "x86-01.bsys.centos.org",
        "relocations": "(not relocatable)",
        "packager": "CentOS BuildSystem <http://bugs.centos.org>",
        "vendor": "CentOS",
        "url": "http://ftp.altlinux.org/pub/people/legion/kbd",
        "summary": "Legacy data for kbd package",
        "description": "The kbd-legacy package contains original keymaps for kbd package..."
      },
      ...
    ]
"""
import jc.utils


class info():
    version = '1.0'
    description = '`rpm -qi` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    # details = 'enter any other details here'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux']
    magic_commands = ['rpm -qi', 'rpm -qia', 'rpm -qai']


__version__ = info.version


def process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured data with the following schema:

        [
          {
            "name":             string,
            "epoch":            integer,
            "version":          string,
            "release":          string,
            "architecture":     string,
            "install_date":     string,
            "group":            string,
            "size":             integer,
            "license":          string,
            "signature":        string,
            "source_rpm":       string,
            "build_date":       string,
            "build_epoch":      integer,          # naive timestamp
            "build_epoch_utc":  integer,          # Aware timestamp if timezone is UTC
            "build_host":       string,
            "relocations":      string,
            "packager":         string,
            "vendor":           string,
            "url":              string,
            "summary":          string,
            "description":      string
          }
        ]
    """
    for entry in proc_data:
        
        int_list = ['epoch', 'size']
        for key in int_list:
            if key in entry:
                try:
                    entry[key] = int(entry[key])
                except (ValueError):
                    entry[key] = None

        if 'build_date' in entry:
            timestamp = jc.utils.timestamp(entry['build_date'])
            entry['build_epoch'] = timestamp.naive
            entry['build_epoch_utc'] = timestamp.utc

    return proc_data


def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) output preprocessed JSON if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        List of Dictionaries. Raw or processed structured data.
    """
    if not quiet:
        jc.utils.compatibility(__name__, info.compatible)

    raw_output = []
    entry_obj = {}
    last_entry = None
    this_entry = None
    desc_entry = False
    description = []

    if jc.utils.has_data(data):

        for line in filter(None, data.splitlines()):
            split_line = line.split(': ', maxsplit=1)

            if split_line[0].startswith('Name') and len(split_line) == 2:
                this_entry = split_line[1].strip()

                if this_entry != last_entry:
                    if entry_obj:
                        if description:
                            entry_obj['description'] = ' '.join(description)
                        raw_output.append(entry_obj)
                        entry_obj = {}
                        last_entry = this_entry
                        desc_entry = False

            if len(split_line) == 2:
                entry_obj[split_line[0].strip().lower().replace(' ', '_')] = split_line[1].strip()

            if line.startswith('Description :'):
                desc_entry = True
                description = []
                continue

            if desc_entry:
                description.append(line)

        if entry_obj:
            if description:
                entry_obj['description'] = ' '.join(description)
            raw_output.append(entry_obj)

    if raw:
        return raw_output
    else:
        return process(raw_output)
