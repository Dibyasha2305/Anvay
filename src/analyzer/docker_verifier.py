import subprocess


def verify_docker_container():

    try:
        result = subprocess.run(
            [
                r"C:\Users\Dibyasha\AppData\Local\Programs\DockerDesktop\resources\bin\docker.exe",
                "exec",
                "anvay-ai",
                "python",
                "-c",
                "import requests; print(requests.post('http://localhost:8001/generate', json={'prompt': 'I love this movie'}).json())"
            ],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            return {
                "success": False,
                "message": result.stderr
            }

        return {
            "success": True,
            "message": "Dockerized AI service works",
            "response": result.stdout.strip()
        }

    except Exception as error:

        return {
            "success": False,
            "message": str(error)
        }

