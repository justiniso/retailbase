({
    baseUrl: "src/js",
    stubModules: ['jsx', 'text', 'JSXTransformer'],
    paths: {
        bootstrap: "../../bower_components/bootstrap/dist/js/bootstrap.min",
        jquery: "../../bower_components/jquery/dist/jquery.min",
        react: "../../bower_components/react/react-with-addons",
        JSXTransformer: "lib/JSXTransformer",
        jsx: "lib/jsx"
    },
    name: "main",
    jsx: {
        fileExtension: ".jsx"
    }
})