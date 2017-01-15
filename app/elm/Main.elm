module Main exposing (main)

import Header exposing (header)
import Http
import Json.Decode as Decode exposing (..)
import Json.Encode as Encode exposing (..)
import Task

main =
    header


-- Messages
type Msg
    = SendSentiment
    | GetSentiment String
    | FetchFail Http.Error

{-
update : Msg -> Model -> (Model, Cmd Msg)
update msg model =
    case msg of
        SendSentiment ->
            model ! [sendSentiment model.sentiment]
        GetSentiment value ->
            ( { model | classification = (toString value) }, Cmd.none )
        FetchFail _ ->
            ( { model | sentiment = "", classification = "" }, Cmd.none )
-}
{-
  Model
-}
type alias Model =
    { sentiment : String
    , classification : String
    }


{-
  Update
-}
encodeSentiment : Model -> Encode.Value
encodeSentiment model =
    Encode.object [ ("sentiment", Encode.string model.sentiment ) ]

sendSentiment : Model -> Task.Task Http.Error String
sendSentiment model =
    { verb = "POST"
    , headers = [ ("Content-Type", "application/json") ]
    , url = "http://127.0.0.1:5000/sentiment"
    , body = Http.string <| Encode.encode 0 <| encodeSentiment model
    }
    |> Http.send Http.defaultSettings
    |> Http.fromJson tokenDecoder


tokenDecoder : Decode.Decoder String
tokenDecoder = "classification" := Decode.string

fetchSentimentCmd : Model -> Cmd Msg
fetchSentimentCmd model =
    Task.perform GetSentiment (sendSentiment model)
