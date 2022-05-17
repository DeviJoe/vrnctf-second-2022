FROM gitea/gitea:1.16.7

RUN apk add sudo
RUN echo "git:readKnead" | chpasswd
