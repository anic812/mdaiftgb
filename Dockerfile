FROM archlinux:latest

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8 LANGUAGE=en_US:en TZ=Asia/Kolkata

RUN pacman -Syyu --noconfirm && \
    pacman -S --noconfirm python-pip zstd p7zip gcc git ffmpeg mediainfo libmediainfo libzen sox lame flac libmad libvorbis libmediainfo tinyxml2&& \
    pacman -Syu sox libzen mediainfo --needed && \
    python3 -m venv /venv && \
    pacman -Scc --noconfirm

ENV PATH="/venv/bin:$PATH"
RUN pip3 install -U pip setuptools wheel && \
    mkdir /app
WORKDIR /app

RUN git clone https://github.com/anic812/mdaiftgb.git /app && \
    pip3 install -U -r requirements.txt

RUN sed -i 's/#en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && sudo locale-gen && echo -e 'LANG=en_US.UTF-8\nLC_ALL=en_US.UTF-8' | tee /etc/locale.conf


RUN chmod +x start.sh

CMD ["bash", "start.sh"]
