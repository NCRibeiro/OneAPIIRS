# ────────────────────────────────────────────────
# Stage 1: Builder — Compila Flutter Web
# ────────────────────────────────────────────────
FROM ubuntu:22.04 AS flutter-builder

# Instala dependências essenciais
RUN apt-get update && apt-get install -y \
    curl git unzip xz-utils zip libglu1-mesa \
    && rm -rf /var/lib/apt/lists/*

# Instala o Flutter SDK
RUN git clone https://github.com/flutter/flutter.git -b stable /flutter
ENV PATH="/flutter/bin:/flutter/bin/cache/dart-sdk/bin:${PATH}"

# Prepara o diretório do projeto
WORKDIR /app

# Copia o código do Flutter para dentro da imagem
COPY . .

# Permissão total para evitar problemas com cache/build em ambientes Docker
RUN chmod -R 777 /app

# Habilita build web
RUN flutter config --enable-web

# Resolve dependências
RUN flutter pub get

# Faz o build para web (separado para facilitar debug)
RUN flutter build web --release

# ────────────────────────────────────────────────
# Stage 2: NGINX — Servidor para o app Web
# ────────────────────────────────────────────────
FROM nginx:alpine

# Remove config padrão e adiciona custom (opcional)
RUN rm -rf /usr/share/nginx/html/*
COPY --from=flutter-builder /app/build/web /usr/share/nginx/html

# Expõe a porta 80 para servir o Flutter Web
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
