FROM node:20-alpine
WORKDIR /app
COPY package.json .
RUN npm install --production
COPY index.js .

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD wget -qO- http://localhost:8003/health || exit 1

RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser

EXPOSE 8003
CMD ["node", "index.js"]