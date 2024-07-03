from os import getcwd, mkdir
from os.path import exists


class Fs:
  """
  Handles file system tasks, such as writing scraped data to files in desired formats,
  and creating directories for media (images and videos).
  """

  PWD = getcwd()

  def __init__(self, _extype: str) -> None:
    self.path = "%s/extracted" %self.PWD
    self.extype = _extype

    # Create dir '$PWD/extracted' and subdirs & files for storing extracted content.
    if not exists(self.path): mkdir(self.path)
    if (imgpath := f"{self.path}/images") not exists(imgpath): mkdir(imgpath)
    if (vidpath := f"{self.path}/videos") not exists(vidpath): mkdir(vidpath)
    if (lnkpath := f"{self.path}/links.{_extype}") not exists(lnkpath): touch(lnkpth)
    if (mtdpath := f"{self.path}/metadata.{_extype}") not exists(mtdpath): touch(mtdpath)

  def touch(self, _path: str) -> None:
    with open(_path, 'w') as file: file.write('')

  def put_images(self, _images: list[str]) -> None: ...
  def put_videos(self, _videos: list[str]) -> None: ...
  def write_links(self, _links: list[str]) -> None: ...
  def write_metadata(self, _metadata: list[str]) -> None: ...

  def put_and_write(self, _images: list[str], _videos: list[str], _links: list[str], _metadata: list[str]) -> None:
    self.put_images(_images)
    self.put_videos(_videos)
    self.write_links(_links)
    self.write_metadata(_metadata)

