#!/bin/bash

python model_runner.py 30 scenarios/cu-calibration.json
python model_runner.py 30 scenarios/cu-25-nisol.json
python model_runner.py 30 scenarios/cu-25-yisol.json
python model_runner.py 30 scenarios/cu-50-nisol.json
python model_runner.py 30 scenarios/cu-50-yisol.json
python model_runner.py 30 scenarios/cu-75-nisol.json
python model_runner.py 30 scenarios/cu-75-yisol.json
python model_runner.py 30 scenarios/cu-counterfactual.json
