FROM ubuntu:18.04

RUN apt-get update && apt-get install -y openssh-server
RUN mkdir /var/run/sshd
RUN echo 'root:admin123' | chpasswd
RUN sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

# SSH login fix. Otherwise user is kicked off after login
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

ENV NOTVISIBLE "in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile

EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get install -y locales && rm -rf /var/lib/apt/lists/* \
    && localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8
ENV LANG en_US.utf8

## Base System
RUN dpkg --add-architecture i386 && \
	apt update -y && \
	apt install -y \
		mailutils \
		postfix \
		curl \
		wget \
		file \
		bzip2 \
        openssh-server \
		gzip \
        vim \
		unzip \
		bsdmainutils \
		python \
		util-linux \
		binutils \
		bc \
        netcat \
        jq \
		tmux \
		lib32gcc1 \
		libstdc++6 \
		libstdc++6:i386 \
		apt-transport-https \
		ca-certificates \
		telnet \
		expect \
		libncurses5:i386 \
		libcurl4-gnutls-dev:i386 \
		libstdc++5:i386 \
		lib32tinfo5 \
		xz-utils \
		zlib1g:i386 \
		libldap-2.4-2:i386 \
		lib32z1 \
		iproute2 \
		default-jre \
		speex:i386 \
		libtbb2 \
		libxrandr2:i386 \
		libglu1-mesa:i386 \
		libxtst6:i386 \
		libusb-1.0-0:i386 \
		libopenal1:i386 \
		libpulse0:i386 \
		libdbus-glib-1-2:i386 \
		libnm-glib4:i386 \
		zlib1g \
		libssl1.0.0:i386 \
		libtcmalloc-minimal4:i386 \
		libsdl1.2debian \
		libnm-glib-dev:i386 \
		&& apt-get clean \
	  && rm -rf /var/lib/apt/lists/*
	  
# Add the linuxgsm user
RUN adduser linuxgsm --no-create-home --disabled-password --gecos ""
RUN echo 'linuxgsm:admin123' | chpasswd

## linuxgsm.sh
RUN wget https://linuxgsm.com/dl/linuxgsm.sh -P /home/linuxgsm

## user config
RUN chown linuxgsm:linuxgsm -R /home/linuxgsm
RUN chmod +x /home/linuxgsm/linuxgsm.sh
RUN chmod 755 /home/linuxgsm

# need use xterm for LinuxGSM
ENV TERM=xterm

## Docker Details
ENV PATH=$PATH:/home/linuxgsm

COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["bash","/entrypoint.sh" ]
