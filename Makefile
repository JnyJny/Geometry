
TARGET= Geometry
VERSION= "0.0.1"
QVERSION= "'${VERSION}'"

PYTHON=python3
SETUP= setup.py
PYSETUP= ${PYTHON} ${SETUP}

PKG_ROOT= ${TARGET}
PKG_INIT = ${PKG_ROOT}/__init__.py

SED = sed
RM = rm
MV = mv

UPDTVER = 's/__version__.*/__version__ = ${QVERSION}/'


VERSION: ${PKG_ROOT}/__init__.py
	@echo ${VERSION} > $@
	@${SED} -e ${UPDTVER} ${PKG_INIT} > ${PKG_INIT}.tmp
	@${MV} ${PKG_INIT}.tmp ${PKG_INIT}

sdist:
	${PYSETUP} build sdist

bdist:
	${PYSETUP} build bdist_wheel



clean:
	@${RM} -rf VERSION
