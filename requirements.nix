{ python3, buildPythonPackage, lib, fetchPypi, lxml, requests, pytz, dateutil, future }:

let

tinytag = buildPythonPackage rec {
  pname = "tinytag";
  version = "1.5.0";
  src = fetchPypi {
    inherit pname version;
    sha256 = "sha256:1v7ha13n00bcr19a3qwrjkx8k58l0249ixzswdv2bddk7cjbq6w1";
  };
  doCheck = false;
  meta = with lib; {
    homepage = "https://github.com/devsnd/tinytag";
    description = "Read music meta data and length of MP3, OGG, OPUS, MP4, M4A, FLAC, WMA and Wave files with python 2 or 3";
    license = [ licenses.mit ];
    maintainers = with maintainers; [ truh ];
  };
};

dateutils = buildPythonPackage rec {
  pname = "dateutils";
  version = "0.6.12";
  src = fetchPypi {
    inherit pname version;
    sha256 = "sha256:1wg3f3imjq3snvjccv64h5498pqv9xz664xhni7bsh8mnay91p83";
  };
  propagatedBuildInputs = [
    dateutil
    pytz
  ];
  doCheck = false;
  meta = with lib; {
    homepage = "https://github.com/jmcantrell/python-dateutils";
    description = "Utilities for working with datetime objects.";
    license = [ licenses.bsd0 ];
    maintainers = with maintainers; [ truh ];
  };
};

podgen = buildPythonPackage rec {
  pname = "podgen";
  version = "1.1.0";
  src = fetchPypi {
    inherit pname version;
    sha256 = "sha256:05bkkkxlp9jbpc1vfcvfb44y4z0jk1xxpawp5i78grn0fx1bf49a";
  };
  propagatedBuildInputs = [
    dateutils
    future
    lxml
    pytz
    requests
    tinytag
  ];
  doCheck = false;
  meta = with lib; {
    homepage = "https://podgen.readthedocs.io/en/latest/";
    description = "Clean and simple library which helps you generate podcast RSS feeds";
    license = [ licenses.bsd3 licenses.lgpl3Only ];
    maintainers = with maintainers; [ truh ];
  };
};

in

python3.withPackages (ps: with ps; [
  aiofiles
  fastapi
  podgen
  pydantic
  python-multipart
  sqlalchemy
  uvicorn
])
