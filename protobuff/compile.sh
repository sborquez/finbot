#!/bin/bash

cd ./definitions
for proto_file in *.proto; do
    echo "Compiling $proto_file"
    protoc --python_out='../py' $proto_file
    python ../jsonify.py -f $proto_file -t protobuf -o ../json/$proto_file.json
done