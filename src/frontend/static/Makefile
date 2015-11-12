
# This is the directory of each type of resource (css, js, jsx) and should be adjacent to the src dir
BUILD_SUBDIR=build/
SOURCE_SUBDIR=src/

all:deps build

deps:
	mkdir -p ${BUILD_SUBDIR}
	npm install
	./node_modules/.bin/bower install

build: css-build js-build

### Build Static ###

css-build:
	echo "Building CSS"
	mkdir -p ${BUILD_SUBDIR}/css
	compass compile

js-build:
	echo "Building JS"
	mkdir -p ${BUILD_SUBDIR}/js
	cp node_modules/requirejs/require.js ${BUILD_SUBDIR}/js/_require.js
	./node_modules/.bin/r.js -o config.js out=${BUILD_SUBDIR}/js/main.js optimize=none

### Clean ###

clean:
	echo "Cleaning"
