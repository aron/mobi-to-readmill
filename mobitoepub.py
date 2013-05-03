import os
import sys
import zipfile
import time

from distutils.dir_util import copy_tree

from mobiunpack import unpackBook
from mobiml2html import MobiMLConverter

epub_container = """<?xml version="1.0" encoding="UTF-8" ?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>
"""

def ensure_dir(dir):
  if not os.path.exists(dir):
    os.makedirs(dir)

def write_file(filename, data):
  directory = "/".join(filename.split("/")[:-1])
  ensure_dir(directory)
  file(filename, "w").write(data)

def zip_directory(directory, filename, compression=zipfile.ZIP_DEFLATED, dont_compress=[]):
  zip = zipfile.ZipFile(filename, "w", compression)
  rootlen = len(directory) + 1
  for base, dirs, files in os.walk(directory):
    for file in files:
      filename = os.path.join(base, file)
      file_compression = zipfile.ZIP_STORED if file in dont_compress else compression
      zip.write(filename, filename[rootlen:], file_compression)

def mobi_to_epub(infile, outdir="./tmp"):
  book_name = infile.split(".")[0]
  outdir = "%s/%s" % (outdir, ("%f" % time.time()).replace(".", "_"), )

  # unpack the mobi file
  intermediate_dir = "%s/intermediate" % outdir
  ensure_dir(intermediate_dir)
  unpackBook(infile, intermediate_dir)

  # convert mobi markup
  converter = MobiMLConverter("%s/%s.html" % (intermediate_dir, book_name))
  html = converter.processml()

  # create epub container
  epub_dir = "%s/epub" % outdir
  write_file("%s/META-INF/container.xml" % epub_dir, epub_container)

  # create mimetype file
  write_file("%s/mimetype" % epub_dir, "application/epub+zip")

  # copy everything from the intermediate directory to the epub directory
  epub_content_dir = "%s/OEBPS" % epub_dir
  ensure_dir(epub_content_dir)
  copy_tree(intermediate_dir, epub_content_dir)
  os.rename(
    "%s/%s.opf" % (epub_content_dir, book_name),
    "%s/content.opf" % (epub_content_dir, )
  )

  # create content file
  write_file("%s/%s.html" % (epub_content_dir, book_name), html)

  # create epub
  epub_file = "%s/%s.epub" % (outdir, book_name)
  zip_directory(epub_dir, epub_file, dont_compress=["mimetype"])

  return epub_file

if __name__ == "__main__":
  infile = sys.argv[1]
  
  mobi_to_epub(infile)
