from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

import os
import tempfile
import threading
import uuid

from src.analyzer.backend_analyzer import analyze_backend
from src.analyzer.ai_analyzer import analyze_ai_service
from src.analyzer.contract_matcher import match_contracts
from src.analyzer.project_integrator import integrate_backend
from src.analyzer.docker_e2e_verifier import (
    verify_integrated_project,
    stop_integrated_project
)
from src.analyzer.package_project import package_project


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Stores the state of each analysis job
jobs = {}


def run_analysis_job(
    job_id,
    backend_path,
    ai_path
):
    try:

        # ==================================================
        # 01 — ANALYZING
        # ==================================================

        jobs[job_id]["step"] = "analyzing"
        jobs[job_id]["message"] = (
            "Reading backend and AI service contracts"
        )

        backend_contract = analyze_backend(
            backend_path
        )

        ai_contract = analyze_ai_service(
            ai_path
        )

        analysis = match_contracts(
            backend_contract,
            ai_contract
        )


        # ==================================================
        # 02 — INTEGRATING
        # ==================================================

        jobs[job_id]["step"] = "integrating"
        jobs[job_id]["message"] = (
            "Generating mappings and integration adapter"
        )

        integrated_project = integrate_backend(
            backend_path,
            ai_path,
            backend_contract,
            ai_contract,
            analysis["mappings"]
        )


        # ==================================================
        # 03 — VERIFYING
        # ==================================================

        jobs[job_id]["step"] = "verifying"
        jobs[job_id]["message"] = (
            "Building containers and running "
            "end-to-end test"
        )

        verification = verify_integrated_project()


        # Always stop generated containers after test
        stop_integrated_project()


        # ==================================================
        # VERIFICATION FAILED
        # ==================================================

        if not verification["success"]:

            jobs[job_id]["step"] = "failed"

            jobs[job_id]["message"] = (
                verification["message"]
            )

            jobs[job_id]["result"] = {

                "backend": backend_contract,

                "ai_service": ai_contract,

                "mappings": analysis["mappings"],

                "mismatches": analysis["mismatches"],

                "verification": verification,

                "integrated_project": integrated_project,

                "download_available": False
            }

            return


        # ==================================================
        # 04 — PACKAGING
        # ==================================================

        jobs[job_id]["step"] = "packaging"

        jobs[job_id]["message"] = (
            "Creating verified project ZIP"
        )

        zip_path = package_project(
            integrated_project
        )


        # ==================================================
        # COMPLETE
        # ==================================================

        jobs[job_id]["step"] = "complete"

        jobs[job_id]["message"] = (
            "Integration completed successfully"
        )

        jobs[job_id]["result"] = {

            "backend": backend_contract,

            "ai_service": ai_contract,

            "mappings": analysis["mappings"],

            "mismatches": analysis["mismatches"],

            "verification": verification,

            "integrated_project": integrated_project,

            "download_available": (
                os.path.exists(zip_path)
            )
        }


    except Exception as error:

        jobs[job_id]["step"] = "failed"

        jobs[job_id]["message"] = str(error)

        jobs[job_id]["result"] = {

            "verification": {
                "success": False,
                "message": str(error)
            },

            "download_available": False
        }


@app.post("/analyze")
async def analyze(
    backend_file: UploadFile = File(...),
    ai_file: UploadFile = File(...)
):

    # ==================================================
    # Create temporary workspace for uploaded files
    # ==================================================

    temp_dir = tempfile.mkdtemp()

    backend_path = os.path.join(
        temp_dir,
        "backend.py"
    )

    ai_path = os.path.join(
        temp_dir,
        "ai_service.py"
    )


    # Save backend upload
    with open(
        backend_path,
        "wb"
    ) as file:

        file.write(
            await backend_file.read()
        )


    # Save AI service upload
    with open(
        ai_path,
        "wb"
    ) as file:

        file.write(
            await ai_file.read()
        )


    # ==================================================
    # Create analysis job
    # ==================================================

    job_id = str(
        uuid.uuid4()
    )

    jobs[job_id] = {

        "step": "starting",

        "message": "Starting Anvay",

        "result": None
    }


    # ==================================================
    # Run heavy processing in background
    # ==================================================

    thread = threading.Thread(
        target=run_analysis_job,
        args=(
            job_id,
            backend_path,
            ai_path
        ),
        daemon=True
    )

    thread.start()


    # Return immediately to frontend
    return {

        "job_id": job_id,

        "step": "starting",

        "message": "Anvay started"
    }


@app.get("/status/{job_id}")
def get_status(
    job_id: str
):

    job = jobs.get(
        job_id
    )

    if job is None:

        return {

            "success": False,

            "message": "Job not found"
        }


    response = {

        "job_id": job_id,

        "step": job["step"],

        "message": job["message"]
    }


    # Add final result when available
    if job["result"] is not None:

        response["result"] = job["result"]


    return response


@app.get("/download")
def download_project():

    zip_path = os.path.abspath(
        "generated/anvay-integrated-project.zip"
    )


    if not os.path.exists(zip_path):

        return {

            "success": False,

            "message": (
                "No verified integrated project found"
            )
        }


    return FileResponse(

        path=zip_path,

        filename="anvay-integrated-project.zip",

        media_type="application/zip"
    )