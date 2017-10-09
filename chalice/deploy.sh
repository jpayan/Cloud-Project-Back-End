#!/usr/bin/env bash

PROFILE=$1

if [ -z "$PROFILE" ]
then
    PROFILE=default
fi

echo "Deploying project..."
LIB_PATH=chalicelib

# Clean directory
if [ -f $LIB_PATH ]; then
    rm -R $LIB_PATH
fi
if [ -f requirements.txt ]; then
    rm requirements.txt
fi

# Copy python content to chalicelib
mkdir -p $LIB_PATH
cp -R ../python/project $LIB_PATH/

# Copy main requirements.txt file
cp ../requirements.txt ./requirements.txt

# Deploy Lambda function
chalice deploy --profile $PROFILE --no-autogen-policy