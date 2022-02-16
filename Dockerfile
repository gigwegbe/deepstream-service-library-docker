ARG BASE_IMAGE=nvcr.io/nvidia/deepstream-l4t:6.0-samples
FROM ${BASE_IMAGE}

ARG REPOSITORY_NAME=dsl-demo

ENV DEBIAN_FRONTEND=noninteractive
ENV LANG C.UTF-8
ENV PATH="/usr/local/cuda/bin:${PATH}"
ENV LD_LIBRARY_PATH="/usr/local/cuda/lib64:${LD_LIBRARY_PATH}"


WORKDIR /tmp



RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        libgstreamer1.0-dev \
        libgstreamer-plugins-base1.0-dev \
        libjson-glib-dev \
        libssl-dev \
        graphviz && \
    rm -rf /var/lib/apt/lists/*


RUN apt install \
	libgstreamer1.0-0 \
	gstreamer1.0-tools \
	gstreamer1.0-plugins-good \
	gstreamer1.0-plugins-bad \
	gstreamer1.0-plugins-ugly \
	gstreamer1.0-libav \
	libgstrtspserver-1.0-0 \
	libjansson4=2.11-1


RUN mkdir /${REPOSITORY_NAME}

WORKDIR /${REPOSITORY_NAME}

RUN apt-get update
RUN apt-get install libgstrtspserver-1.0-dev gstreamer1.0-rtsp
RUN apt-get install -y libgeos-dev 
RUN apt-get update
#RUN apt-get install -y python3-opencv
RUN apt-get install -y  vim
RUN apt-get update
RUN apt-get install -y libcurl4-openssl-dev
RUN apt-get install -y graphviz imagemagick
RUN apt-get install -y doxygen
RUN apt-get install -y unzip
RUN apt-get update
RUN apt-get install -y build-essential cmake git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev
RUN apt-get install -y libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev
RUN apt-get install -y python2.7-dev python3.6-dev python-dev python-numpy python3-numpy
RUN apt-get install -y libtbb2 libtbb-dev libjpeg-dev libpng-dev libtiff-dev libdc1394-22-dev
RUN apt-get install -y libv4l-dev v4l-utils qv4l2 v4l2ucp
RUN apt-get install -y curl
#RUN apt install vlc
RUN apt-get install -y python3-pip
RUN apt-get install -y python-pip
RUN pip3 install --upgrade pip 
RUN apt-get install -y python3-opencv
RUN pip3 install numpy==1.19.4 
RUN apt-get install -y  libapr1 libapr1-dev libaprutil1 libaprutil1-dev
RUN apt-get update
RUN apt install -y libgeos-dev 
RUN apt install -y libcurl4-openssl-dev
RUN apt install -y libjson-glib-1.0-0
RUN apt install -y libsoup-gnome2.4-dev
RUN apt install -y graphviz imagemagick
RUN apt install -y doxygen
RUN apt-get install -y libopencv-dev 
RUN cp -r /usr/lib/aarch64-linux-gnu/pkgconfig/opencv.pc /usr/lib/aarch64-linux-gnu/pkgconfig/opencv4.pc

RUN apt-get update
#RUN cd /dsl-demo/
WORKDIR /${REPOSITORY_NAME}
RUN apt-get install -y apache2-dev
#RUN git clone https://github.com/prominenceai/deepstream-services-library.git -Future works
#WORKDIR /${REPOSITORY_NAME}/deepstream-services-library -Future works
RUN ldconfig
RUN apt --fix-broken install
RUN apt-get install libapr1 libapr1-dev
RUN apt-get update
#COPY Makefile  /${REPOSITORY_NAME}/dsl-Future works
#RUN make -j4
COPY hlkv1 /${REPOSITORY_NAME}/dslv1
RUN unzip -o /${REPOSITORY_NAME}/dslv1/test.zip
RUN rm -rf /${REPOSITORY_NAME}/dslv1/test.zip
#RUN cp -r  /opt/nvidia/deepstream/deepstream/lib/libnvds_nvmultiobjecttracker.so /opt/nvidia/deepstream/deepstream/lib/libnvds_mot_iou.so