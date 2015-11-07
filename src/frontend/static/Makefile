
# This is the directory of each type of resource (css, js, jsx) and should be adjacent to the src dir
BUILD_SUBDIR=build/
SOURCE_SUBDIR=src/

all:deps build

deps:
	npm install
	./node_modules/.bin/bower install

build: css-build js-build

### Build Static ###

css-build:
	echo "Building CSS"
	compass compile

js-build:
	echo "Building JS"
	cp node_modules/requirejs/require.js ${BUILD_SUBDIR}/js/_require.js
	./node_modules/.bin/r.js -o config.js out=${BUILD_SUBDIR}/js/main.js optimize=none

### Clean ###

clean:
	echo "Cleaning"
