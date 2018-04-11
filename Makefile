RPMBUILD_TGZ=rpmbuild --tb
RPMBUILD_ROOT=${HOME}/rpmbuild/

NAME=cronsun
VERSION=0.1.0
SRCPATH=${NAME}-${VERSION}
SRCFILE=${NAME}-${VERSION}.tgz

all:fetch build copy

fetch:
	rm -rf ../${SRCPATH} ../${SRCFILE}
	cp -r ../cronsun ../${SRCPATH}
	cd .. && tar -czf ${SRCFILE} ${SRCPATH}

build:
	${RPMBUILD_TGZ} ../${SRCFILE}

copy:
	cp ${RPMBUILD_ROOT}/RPMS/*/${NAME}*${VERSION}*.rpm .