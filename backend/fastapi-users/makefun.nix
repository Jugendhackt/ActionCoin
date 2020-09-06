{ lib, buildPythonPackage, setuptools_scm, fetchPypi, pymongo, pytest
, pytestrunner, setuptools, six }:

buildPythonPackage rec {
  pname = "makefun";
  version = "1.9.3";

  src = fetchPypi {
    inherit pname version;
    sha256 = "709ea9ab8e8c98ac3a12a464d75748d5161a8752a2bf79daaf02f5f7e8b66132";

  };

  nativeBuildInputs = [ pytestrunner setuptools_scm six ];
  propagatedBuildInputs = [ setuptools pymongo ];

  buildPhase = "";

  doCheck = false;
  checkInputs = [ pytest ];
  checkPhase = ''
    py.test -k 'not function_name and not other_function' tests
  '';

  meta = with lib; {
    homepage = "https://github.com/smarie/python-makefun";
    description = "Small library to dynamically create python functions.";
    license = licenses.bsd3;
    maintainers = "maksim";
  };
}
