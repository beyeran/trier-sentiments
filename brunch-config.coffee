module.exports =
  config:
    paths:
      watched: ["app"]
      public: 'static'

    files:
      javascripts:
        joinTo: "js/app.js"

      stylesheets:
        joinTo: "css/app.css"
      
    plugins:
      elmBrunch:
        mainModules: ["app/elm/Main.elm"]
        outputFolder: "static/js/"

      sass:
        mode: "native"

