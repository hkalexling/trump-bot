#! /bin/bash

docker run -t --rm -p 8501:8501 \
    -v "/home/alex_ling/trump-bot/model:/models/speech/1" \
    -e MODEL_NAME=speech \
    tensorflow/serving
