module Header exposing (..)

import Html exposing (div, h1, ul, li, a, text, textarea)
import Html.Attributes exposing (id, href)

header =
    div [ id "content" ] [
         div [ id "header" ] [
              h1 [] [ text "Trier Sentiments" ]
             ],
             div [ id "main" ] [
                  textarea [] [ text "Type here..." ]
                 ],
             div [ id "output" ] []
        ]
    
