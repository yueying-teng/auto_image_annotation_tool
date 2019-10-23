docker run -it \
	-v $(pwd)/model:/inception/model \
    -v $(pwd)/data:/inception/data \
    -v $(pwd)/scripts:/inception/scripts \
    -v $(pwd)/output:/inception/output \
    -p 8080:8080 \
    -p 8501:8501 \
    --rm yyyyteng/inception_ffmpeg bash
