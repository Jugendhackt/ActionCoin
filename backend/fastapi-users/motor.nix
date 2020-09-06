{ lib, buildPythonPackage, fetchFromGitHub, pymongo }:

buildPythonPackage rec {
  pname = "motor";
  version = "2.2.0";

  src = fetchFromGitHub {
    owner = "mongodb";
    repo = "motor";
    rev = version;
    sha256 = "16bwqhhwrhrzpq21hxmzwwcm0agy6yl29m7g16yg1fb80bn3vw86";
  };

  propagatedBuildInputs = [ pymongo ];
  doCheck = false;

  meta = with lib; {
    homepage = "https://github.com/mongodb/motor/";
    description = "Non-blocking MongoDB driver for Tornado or asyncio";
    license = licenses.asl20;
    maintainers = "maksim";
  };
}
