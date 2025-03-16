### README.md

# Image Watermarking Tool

This tool processes images by adding a diagonal orange watermark containing their relative path and filename. It uses Python and ImageMagick.

## Requirements
- Docker installed on your system.

## Building the Docker Image

```bash
docker build -t watermark-tool .
```

## Running the Tool (without SELinux)

```bash
docker run --rm -v ./source_images:/app/source_images \
           -v ./destination_images:/app/destination_images \
           -v ./watermark_images:/app/watermark_images \
           watermark-tool --input /app/source_images --output /app/destination_images --logo /app/watermark_images
```

- Replace `./source_images` with your actual local path to source images.
- Replace `./destination_images` with your desired output directory.
- Replace `./watermark_images` with your desired logo directory.

## Running the Tool (with SELinux)
For systems running with SELinux enabled, it is possible that the container will not have permission to mount the local volumes. 

In this situation we need to append :Z to the volume mount.

This is explained in detail [here](https://www.redhat.com/en/blog/user-namespaces-selinux-rootless-containers) in an excellent blog by Dan Walsh.


```bash
docker run --rm -v ./source_images:/app/source_images:Z \
           -v ./destination_images:/app/destination_images:Z \
           -v ./watermark_images:/app/watermark_images:Z \
           watermark-tool --input /app/source_images --output /app/destination_images --logo /app/watermark_images
```

- Replace `./source_images` with your actual local path to source images.
- Replace `./destination_images` with your desired output directory.
- Replace `./watermark_images` with your desired logo directory.



## Notes
- The script will create missing directories in the destination path as needed.
- It prints the progress and a final summary of processed files.

## Troubleshooting
- Ensure the source directory contains readable image files.
- Check Docker permissions if file access errors occur.

---

You're all set to watermark images with ease!

