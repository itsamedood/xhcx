from out import XhcxError
from sys import argv, exit


class Cli:
  """
  Handles CLI things, mainly arguments passed to the program.
  """

  HELP = """X Hypertext Content eXtractor (xhcx)
  Usage: xhcx --[flags] <url>
  Flags:
    extype=type - Export type (json,yaml,xml,plaintext). Default is json.
    verbose     - Enables verbose output for debugging purposes.
    help        - Displays this help menu.
    version     - Displays installed version of xhcx.
"""

  VERSION = "0.0.1"

  flags: dict[str, str | bool] = {
    "extype": "json",
    "verbose": False
  }

  def __init__(self) -> None: ...

  def read(self) -> tuple[dict[str, str | bool], str | None]:  # Value type might change over time!
    """
    Gets flags from command line,
    splits them into 2 groups (ones with values, & ones without),
    and processes them.
    """

    flags = [a[2:] for a in argv if a[:2] == "--"]  # All elements of argv that start with "--".

    # Flag name (0) & value (1).
    valflags=[(f := flag.split('='), f[0], f[1]) for flag in flags if '=' in flag] if len(flags) > 0 else None

    # None if last element starts with "--".
    url = (argv[-1] if (u := argv[-1]) and not u[:2] == "--" and not u == argv[0] else None)

    self.process_flags(flags)
    self.process_vflags(valflags)

    return (self.flags, url)

  def process_flags(self, _flags):
    """
    Process flags that don't have a value.
    """

    _flags = [f for f in _flags if '=' not in f]

    for flag in _flags:
      match flag:
        # Flags that affect program behavior.
        case "verbose": self.flags[flag] = True

        # Flags that should exit after being processed.
        case "help":
          print(self.HELP)
          exit(0)

        case "version":
          print(self.VERSION)
          exit(0)

        case _: raise XhcxError("invalid flag: '%s'" %flag)

  def process_vflags(self, _vflags: list[tuple[list[str], str, str]] | None):
    """
    Processes flags that require a value.
    """

    if _vflags is None: return
    for (fsplit, fname, fvalue) in _vflags:
      match fname:
        case "extype":
          if fvalue in ["json", "yaml", "xml", "plaintext"]: self.flags[fname] = fvalue
          else: raise XhcxError("invalid extype: '%s'" %fvalue)

        case _: raise XhcxError("invalid flag: '%s'" %fname)
