import os
import re
from pathlib import Path
import logging
import datetime

import botocore
import joblib
import yaml
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

import src.aws_utils as aws
import src.present_interface as pi

import streamlit as st

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

artifacts = Path() / "artifacts"

BUCKET_NAME = os.getenv("BUCKET_NAME", "cloud-project-models")
# ARTIFACTS_PREFIX = os.getenv("ARTIFACTS_PREFIX", "artifacts/")
CONFIG_REF = os.getenv("CONFIG_REF", "config/config.yml")


def load_config(config_ref: str) -> dict:
    if config_ref.startswith("s3://"):
        # Get config file from S3
        config_file = Path("config/downloaded-config.yaml")
        try:
            bucket, key = re.match(r"s3://([^/]+)/(.+)", config_ref).groups()
            aws.download_s3(bucket, key, config_file)
        except AttributeError:  # If re.match() does not return groups
            print("Could not parse S3 URI: ", config_ref)
            config_file = Path("config/default.yaml")
        except botocore.exceptions.ClientError as e:  # If there is an error downloading
            print("Unable to download config file from S3: ", config_ref)
            print(e)
    else:
        # Load config from local path
        config_file = Path(config_ref)
    if not config_file.exists():
        raise EnvironmentError(f"Config file at {config_file.absolute()} does not exist")

    with config_file.open() as f:
        return yaml.load(f, Loader=yaml.SafeLoader)


def main():
    config = load_config(CONFIG_REF)
    run_config = config.get("run_config", {})
    print(run_config)
    # Set up output directory for saving artifacts
    artifacts = Path(run_config.get("output", "runs"))
    
    model_s3_key = config["aws"]["selected_model_key"]
    
    @st.cache_resource
    def load_model():
        print("loading artifacts from: ", artifacts.absolute())
        # Download files from S3
        aws.download_s3(BUCKET_NAME, model_s3_key, artifacts / model_s3_key)
        
        # Load model from the downloaded file
        model = joblib.load(artifacts / model_s3_key)
        
        return model
    
    model = load_model()
    
    # TODO: feed user input to scores
    scores = []

    # Present user interface
    pi.present_interface(scores)

if __name__ == "__main__":
    main()