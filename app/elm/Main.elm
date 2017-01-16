module Main exposing (main)

-- import Header exposing (header)
import Html exposing (..)
import Html.Attributes exposing (..)
import Html.Events exposing (..)
import Html.App exposing (..)
import Http
import HttpBuilder exposing (..)
import Json.Decode as Decode exposing (..)
import Json.Decode.Pipeline as JsonPipeline exposing (decode, required)
import Json.Decode.Extra exposing ((|:))
import Json.Encode as Encode exposing (..)
import Task

main =
    Html.App.program
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
        , p [] [ text model.classification ]
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
init = (Model "what a terrible movie" "", Cmd.none )

-- update
type Msg = Submit
         | FetchSucceed JSONResponse
         | FetchFail Http.Error

update : Msg -> Model -> (Model, Cmd Msg)
update msg model =
    case msg of
        Submit ->
            (model, fetchSentiment model.sentiment)

        FetchSucceed response->
            (Model model.sentiment response.classification, Cmd.none)

        FetchFail error ->
            (model, Cmd.none)

-- http
jsonify : String -> Http.Body
jsonify str =
    let
        json = Encode.encode 0 <| Encode.object [("sentiment", Encode.string str)]
    in
        Http.string json

decodeJson : Decode.Decoder JSONResponse
decodeJson =
    decode JSONResponse
        |> JsonPipeline.required "sentiment" Decode.string
        |> JsonPipeline.required "status" Decode.int

decodeSentiment : String -> Platform.Task Http.Error JSONResponse
decodeSentiment sentiment =
    Http.post decodeJson "http://127.0.0.1:5000/sentiment" (jsonify sentiment)

fetchSentiment : String -> Cmd Msg
fetchSentiment sentiment =
    Task.perform FetchFail FetchSucceed (decodeSentiment sentiment)
