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
        options:
          includePaths: ["node_modules/bootstrap-sass/assets/stylesheets/"],
          precision: 8

      copycat:
        "fonts": ["node_modules/bootstrap-sass/assets/fonts/bootstrap"]

    npm:
      enabled: true,
      globals:
        $: 'jquery',
        jQuery: 'jquery',
        bootstrap: 'bootstrap-sass'