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
    div [class "wrapper"]
        [ div [class "content"] [
               h2 [] [text "Trier Sentiments"]
              , inputArea
              , br [] []
              , viewResult model
              ]
        ]

inputArea : Html Msg
inputArea =
    textarea [ placeholder "Type here...", onInput Submit ] []

viewResult : Model -> Html Msg
viewResult model =
    let
        color =
            case model.classification of
                "negative"          -> "red"
                "somewhat negative" -> "red"
                "neutral"           -> "grey"
                "somewhat positive" -> "green"
                "positive"          -> "green"
                _                   -> "grey"
    in
        div [class "result"] [
             div [ style [("color", color)] ] [ text model.classification ]
            ]

-- model
type alias Model =
    { sentiment : String
    , classification : String
    }

type alias JSONResponse =
    { classification : String
    , status : Int
    }

init : (Model, Cmd Msg)
init = (Model "" "", Cmd.none)

-- update
type Msg = Submit String
         | Fetch (Result Http.Error JSONResponse)


update : Msg -> Model -> (Model, Cmd Msg)
update msg model =
    case msg of
        Submit str ->
            (Model str model.classification, fetchSentiment str Fetch)

        Fetch (Ok res) ->
            (Model "" res.classification, Cmd.none)

        Fetch (Err _) ->
            (model, Cmd.none)


-- http
jsonify : String -> String
jsonify str =
    "{\"sentiment\":\"" ++ str ++ "\"}"

decodeJson : Decode.Decoder JSONResponse
decodeJson =
    Decode.map2 JSONResponse
        (Decode.field "classification" Decode.string)
        (Decode.field "status" Decode.int)


fetchSentiment : String -> (Result Http.Error JSONResponse -> Msg) -> Cmd Msg
fetchSentiment str msg =
    Http.post "http://127.0.0.1:5000/sentiment"
        (Http.stringBody "application/json" <| jsonify str)
        decodeJson
        |> Http.send msg
