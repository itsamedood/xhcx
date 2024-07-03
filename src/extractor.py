from lxml.html import fromstring, HtmlElement
from requests import RequestException, get, head
from out import XhcxDebugNote, XhcxError
from urllib.parse import urlparse


class Extractor:
  """
  Extracts content from given URL using [lxml](https://lxml.de/).

  Includes:
  - Images
  - Videos
  - Links
  - Metadata
  - HTML code
  - CSS code
  - JS code
  """

  def __init__(self, _flags: dict[str, str | bool], _url: str) -> None:
    self.flags = _flags
    self.url = _url
    self.verbose = bool(_flags["verbose"])

  def validate_url(self) -> bool:
    """
    Validates that the url exists and can be reached and can be read as html.
    """

    # Validate url structure.
    purl = urlparse(self.url)

    if not all([purl.scheme, purl.netloc]): raise XhcxError("url structure is invalid")

    # Check if url is accessible.
    try:
      response = head(self.url, allow_redirects=True, timeout=5)
      if response.status_code == 200:
        # Check if content type is html.
        ctype = response.headers.get("Content-Type", '')
        if "text/html" in ctype: return True

    except: raise XhcxError("'%s' is not accessible. check the url and your connection" %self.url)
    finally: return False

  def fetch_page(self) -> bytes:
    response = get(self.url)

    if (status := response.status_code) == 200:  # 200 = no errors
      content = response.content
      XhcxDebugNote(self.verbose, content)
      return content

    else: raise XhcxError(f"Failed to fetch '{self.url}' ({status})" %self.url)

  def parse_html(self, _page_data: bytes) -> HtmlElement:
    return fromstring(_page_data)

  def extract_images(self, _tree: HtmlElement): return _tree.xpath("//img/@src")

  def extract_videos(self, _tree: HtmlElement):
    vids = _tree.xpath("//video/@src")
    srcs = _tree.xpath("//video/source/@src")

    return vids + srcs

  def extract_links(self, _tree: HtmlElement): return _tree.xpath("//a/@href")
  def extract_metadata(self, _tree: HtmlElement): return [m for m in _tree.xpath("//meta")]

  def extract_html_code(self, _tree: HtmlElement): ...
  def extract_css_code(self, _tree: HtmlElement): ...
  def extract_js_code(self, _tree: HtmlElement): ...

  def extract(self) -> tuple[list[str], list[str], list[str], list[HtmlElement], None, None, None]:
    """ Extracts everything from given url. """

    self.validate_url()
    tree = self.parse_html(self.fetch_page())

    return (
      self.extract_images(tree),
      self.extract_videos(tree),
      self.extract_links(tree),
      self.extract_metadata(tree),
      self.extract_html_code(tree),
      self.extract_css_code(tree),
      self.extract_js_code(tree)
    )
