CMAKE_MINIMUM_REQUIRED(VERSION 2.8)

include(RezBuild)


rez_install_files(
	bin/hellorc
	DESTINATION .
	EXECUTABLE
)
