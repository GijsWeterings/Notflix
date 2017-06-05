#!/bin/bash

for filename in ingest/*; do
  if [$filename == "ingest/.gitkeep"]; then
    continue
  fi
  outputFile=${filename/ingest/videos}
  outputFile=${outputFile/mkv/mp4}
  ffmpeg -i ./$filename -vcodec h264 -acodec aac -strict -2 $outputFile
done
