FROM continuumio/miniconda3

# Create working directory
WORKDIR /app

# Copy environment file and build env
COPY environment.yml .
RUN conda env create -f environment.yml

# Activate environment
ENV PATH /opt/conda/envs/azure_speech_env/bin:$PATH

# Copy all source code
COPY . .

# Expose the Flask port
EXPOSE 5000

# Run the app
CMD ["python", "main.py"]
