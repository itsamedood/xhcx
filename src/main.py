from cli import Cli
from extractor import Extractor
from out import XhcxDebugNote, XhcxError


if __name__ == "__main__":
  cli = Cli()
  flags, url = cli.read()
  verbose = bool(flags["verbose"])
  XhcxDebugNote(verbose, flags, url)

  if url is None: raise XhcxError("no url given")

  ext = Extractor(flags, url)
  imgs, vids, links, metadata, html_code, css_code, js_code = ext.extract()

  print(imgs, vids, links, [m.attrib for m in metadata], sep='\n\n')
