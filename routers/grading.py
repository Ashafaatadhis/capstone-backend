from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks, Form
import shutil
import uuid
import os
import requests
from utils.response import success_response
from services.grading_service import GradingService
import json


router = APIRouter(prefix="/grade", tags=["Grading"])


@router.post("/")
async def grade_video(
    background: BackgroundTasks,
    file: UploadFile = File(...),
    callback_url: str = Form(...),
    question_id: int = Form(...)
):
    # Validasi file
    if not file.filename.lower().endswith((".mp4", ".mov", ".mkv", ".avi", ".webm")):
        raise HTTPException(400, "Invalid file format. Please upload a video file.")

    # Simpan file sementara
    ext = os.path.splitext(file.filename)[1].lower()
    temp_name = f"upload_{uuid.uuid4().hex}{ext}"

    with open(temp_name, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    job_id = uuid.uuid4().hex

    # Jalankan background task
    background.add_task(
        process_in_background,
        temp_name,
        callback_url,
        job_id,
        question_id,
    )

    return success_response(
        data={"job_id": job_id},
        message="Grading started"
    )


def process_in_background(video_path, callback_url, job_id, question_id):
    try:
        result = GradingService.process_video(video_path, question_id)

        payload = {
            "job_id": job_id,
            "question_id": question_id,
            "status": "completed",
            "result": result,
        }

    except Exception as e:
        payload = {
            "job_id": job_id,
            "question_id": question_id,
            "status": "error",
            "message": str(e),
        }

    # Callback ke FE
    try:
        print("=== SENDING CALLBACK ===")
        print("URL:", callback_url)
        print("Payload:", json.dumps(payload, indent=2, ensure_ascii=False))

        response = requests.post(callback_url, json=payload, timeout=5)

        # Print hasil request
        print("=== CALLBACK RESPONSE ===")
        print("Status Code:", response.status_code)
        print("Response Body:", response.text)
        print("=========================\n")

    except Exception as callback_error:
        print("Callback failed:", callback_error)


    # Hapus file temp
    if os.path.exists(video_path):
        os.remove(video_path)


# from fastapi import APIRouter, UploadFile, File, HTTPException
# from services.grading_service import GradingService
# import shutil
# import uuid
# import os
# from utils.response import success_response

# router = APIRouter(prefix="/grade", tags=["Grading"])


# @router.post("/")
# async def grade_video(file: UploadFile = File(...)):
#     # only allow video files
#     if not file.filename.lower().endswith((".mp4", ".mov", ".mkv", ".avi", ".webm")):
#         raise HTTPException(400, "Invalid file format. Please upload a video file.")

#     # save temp file
#     ext = os.path.splitext(file.filename)[1].lower()
#     temp_name = f"upload_{uuid.uuid4().hex}{ext}"   
#     with open(temp_name, "wb") as buffer:
#         shutil.copyfileobj(file.file, buffer)

#     try:
#         # run grading pipeline
#         result = GradingService.process_video(temp_name)
#     except Exception as e:
#         raise HTTPException(500, f"Error during grading: {str(e)}")

#     # cleanup
#     if os.path.exists(temp_name):
#         os.remove(temp_name)
 
#     return success_response(data=result, message="Grading completed")
