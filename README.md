# Connecting the Dots Challenge – Adobe India Hackathon

## How to Run

### Build
docker build --platform linux/amd64 -t adobehack:solution .

### Run Round 1A
docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output --network none adobehack:solution

### Run Round 1B
docker run --rm ^
-e PERSONA="PhD Researcher in Computational Biology" ^
-e JOB="Prepare a literature review focusing on methodologies, datasets, and performance benchmarks" ^
-v $(pwd)/input:/app/input ^
-v $(pwd)/output:/app/output ^
--network none adobehack:solution ^
python persona_ranking.py
