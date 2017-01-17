module Main exposing (main)

-- import Header exposing (header)
import Html exposing (..)
import Html.Attributes exposing (..)
import Html.Events exposing (..)
import Http
import HttpBuilder exposing (..)
import Json.Decode as Decode exposing (..)
import Json.Encode as Encode exposing (..)
import Task

main =
    Html.program
        { init = init
        , view = view
        , update = update
        , subscriptions = subscriptions
        }

subscriptions : Model -> Sub Msg
subscriptions model = Sub.none

-- view
view : Model -> Html Msg
view model =
    div []
        [ h2 [] [text "just a damn test"]
        , button [ onClick Submit ] [ text "Classify" ]
        , br [] []
        , pre [] [ text "foo" ]
        , pre [] [ text model.classification ]
        ]

-- model
type alias Model =
    { sentiment : String
    , classification : String
    }


init : (Model, Cmd Msg)
init = (Model "what a terrible movie" "", Cmd.none)

-- update
type Msg = Submit
         | Fetch (Result Http.Error String)

update : Msg -> Model -> (Model, Cmd Msg)
update msg model =
    case msg of
        Submit ->
            (model, fetchSentiment model.sentiment)

        Fetch (Ok res) ->
            (Model "" res, Cmd.none)

        Fetch (Err _) ->
            (model, Cmd.none)

-- http
jsonify : String -> Http.Body
jsonify str =
    Http.jsonBody <| Encode.object [("sentiment", Encode.string str)]

decodeJson : Decode.Decoder String
decodeJson =
    Decode.map2 (\classification status -> classification)
        (Decode.field "classification" Decode.string)
        (Decode.field "status" Decode.int)

fetchSentiment : String -> Cmd Msg
fetchSentiment sentiment =
    Http.send Fetch (Http.post "http//127.0.0.1:5000/sentiment" (jsonify sentiment) decodeJson)
