FROM postgres:12-alpine
ENV GOSU_VERSION 1.10
RUN apk add --no-cache su-exec
RUN apk add --update iputils
COPY ./docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["su-exec", "postgres", "postgres"]
