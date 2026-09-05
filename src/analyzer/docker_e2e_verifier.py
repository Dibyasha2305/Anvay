import os
import subprocess
import time
import requests


DOCKER_BIN = os.path.join(
    os.environ["LOCALAPPDATA"],
    "Programs",
    "DockerDesktop",
    "resources",
    "bin"
)

DOCKER_EXE = os.path.join(
    DOCKER_BIN,
    "docker.exe"
)


def get_docker_env():
    env = os.environ.copy()

    env["PATH"] = (
        DOCKER_BIN
        + os.pathsep
        + env.get("PATH", "")
    )

    return env


def verify_integrated_project():

    project_dir = "generated/integrated_project"
    env = get_docker_env()

    try:

        # Build and start the generated project
        subprocess.run(
            [
                DOCKER_EXE,
                "compose",
                "up",
                "--build",
                "-d"
            ],
            cwd=project_dir,
            env=env,
            check=True
        )

        # Poll the backend instead of blindly waiting 5 seconds
        test_url = "http://localhost:8000/predict"

        max_attempts = 20

        for attempt in range(max_attempts):

            try:

                response = requests.post(
                    test_url,
                    json={
                        "input": "I love this movie"
                    },
                    timeout=3
                )

                if response.status_code == 200:
                    break

            except requests.RequestException:
                pass

            time.sleep(0.5)

        else:

            return {
                "success": False,
                "message": (
                    "Integrated backend did not become "
                    "available in time"
                )
            }

        data = response.json()

        if "prediction" not in data:

            return {
                "success": False,
                "message": (
                    "Missing prediction in response"
                )
            }

        if "confidence" not in data:

            return {
                "success": False,
                "message": (
                    "Missing confidence in response"
                )
            }

        return {
            "success": True,
            "message": (
                "Integrated project works end-to-end"
            ),
            "response": data
        }

    except subprocess.CalledProcessError as error:

        return {
            "success": False,
            "message": (
                f"Docker Compose failed: {error}"
            )
        }

    except Exception as error:

        return {
            "success": False,
            "message": str(error)
        }


def stop_integrated_project():

    project_dir = "generated/integrated_project"
    env = get_docker_env()

    subprocess.run(
        [
            DOCKER_EXE,
            "compose",
            "down"
        ],
        cwd=project_dir,
        env=env
    )