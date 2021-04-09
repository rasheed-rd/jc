"""jc - JSON CLI output utility `foo` command output parser

<<Short foo description and caveats>>

Usage (cli):

    $ foo | jc --foo

    or

    $ jc foo

Usage (module):

    import jc.parsers.foo
    result = jc.parsers.foo.parse(foo_command_output)

Compatibility:

    'linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd'

Examples:

    $ foo | jc --foo -p
    []

    $ foo | jc --foo -p -r
    []
"""
import jc.utils


class info():
    version = '1.0'
    description = '`foo` command parser'
    author = 'John Doe'
    author_email = 'johndoe@gmail.com'
    # details = 'enter any other details here'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']
    magic_commands = ['foo']


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
            "foo":     string,
            "bar":     boolean,
            "baz":     integer
          }
        ]
    """

    # rebuild output for added semantic information
    return proc_data


def filter_lines(line):
    if (line.startswith('Folder') or
            line.startswith('=') or line.startswith('TaskName')):
        return False
    return True


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

    if jc.utils.has_data(data):
        table = ['TaskName                                 Next_Run_Time         Status']
        lines = data.split("\n")
        for line in filter(filter_lines, lines):
            if not line:
                print(table)
                parsed_table = jc.parsers.universal.sparse_table_parse(table)
                # parsed_table = [(item['Folder'] = line) for item in parsed_table]
                if parsed_table:
                    print(parsed_table)
                table = ['TaskName                                 Next_Run_Time         Status']

                # TODO: add folder to output as a field.Right now we're filtering it out.

                continue

            # TODO: handle tables with single line message e.g. INFO:...

        # if not line.startswith('Folder') and not line.startswith('=') and not line.startswith('TaskName'):
        table.append(line)

    if raw:
        return raw_output
    else:
        return process(raw_output)
