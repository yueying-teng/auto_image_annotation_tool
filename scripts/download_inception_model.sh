#!/bin/bash
#
# Copyright 2016 The Open Images Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
#
# Download and extract pretrained Inception v3 model.

set -ue

cd $(cd -P -- "$(dirname -- "$0")" && pwd -P)
cd ../model

model=/inception/model/model_2016_08.tar.gz

if [ -f "$model" ]; then
	echo "model exists"
else
	echo "download model"
	wget https://storage.googleapis.com/openimages/2016_08/model_2016_08.tar.gz
	tar -xzf model_2016_08.tar.gz
fi
