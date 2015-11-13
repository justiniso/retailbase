
BUILD_SUBDIR=build/
SOURCE_SUBDIR=src/
PUBLIC_STATIC_DIR=../../assets

all:deps build

deps:
	mkdir -p ${BUILD_SUBDIR}
	npm install
	./node_modules/.bin/bower install

build: css-build js-build static-finalize

### Build Static ###

css-build:
	echo "Building CSS"
	mkdir -p ${BUILD_SUBDIR}/css
	compass compile
	mv ${BUILD_SUBDIR}/css/styles.css ${BUILD_SUBDIR}/css/main.css

js-build:
	echo "Building JS"
	mkdir -p ${BUILD_SUBDIR}/js
	cp node_modules/requirejs/require.js ${BUILD_SUBDIR}/js/require.js
	./node_modules/.bin/r.js -o config.js out=${BUILD_SUBDIR}/js/main.js optimize=none

static-finalize:
	rm -rf ${PUBLIC_STATIC_DIR}/*
	cp -R ${BUILD_SUBDIR} ${PUBLIC_STATIC_DIR}


### Clean ###

clean:
	echo "Cleaning"
