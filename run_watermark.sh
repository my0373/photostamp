#!/bin/bash

docker run --rm -v ./source_images:/app/source_images:Z \
           -v ./destination_images:/app/destination_images:Z \
           -v ./watermark_images:/app/watermark_images:Z \
            watermark-tool --input /app/source_images \
                --output /app/destination_images \
                --logo /app/watermark_images \
                --resize=facebook
