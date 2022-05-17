FROM tomcat:8.0.36-jre8
RUN mkdir /ctf
WORKDIR /ctf
RUN useradd -M -d /home/ctf ctf

RUN rm -rf /usr/local/tomcat/webapps/*
ADD target/log4shell-1.0-SNAPSHOT.war /usr/local/tomcat/webapps/ROOT.war
ADD target/flag.txt /ctf/flag.txt

RUN chown -R root:ctf /ctf && \
  chmod -R 555 /ctf

RUN chmod -R 777 /usr/local/tomcat
USER ctf
EXPOSE 8080 
CMD ["/usr/local/tomcat/bin/catalina.sh", "run"]
