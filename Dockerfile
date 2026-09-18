# Build stage
FROM node:18 as frontend-builder
WORKDIR /app/spotify-frontend
COPY spotify-frontend/package*.json ./
RUN npm install
COPY spotify-frontend/ .
RUN npm run build

# Runtime stage
FROM python:3.9-slim
WORKDIR /app

# Copy built React frontend
COPY --from=frontend-builder /app/spotify-frontend/build ./spotify-frontend/build

# Copy Python code
COPY src/ ./src/
COPY app.py requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8000

# Run app
CMD ["python3", "app.py"]