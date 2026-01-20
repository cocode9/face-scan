from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from .. import models, schemas, database, auth
import face_recognition
import os
import json
import uuid
from pathlib import Path

router = APIRouter(tags=["auth"], prefix="/auth")

# Create uploads directory if it doesn't exist
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=schemas.UserRead)
async def register(photo: UploadFile = File(...), db: Session = Depends(get_db)):
    # Validate file type
    if not photo.content_type or not photo.content_type.startswith('image/'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an image"
        )
    
    # Generate unique filename
    file_extension = os.path.splitext(photo.filename)[1] if photo.filename else '.jpg'
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = UPLOAD_DIR / unique_filename
    
    try:
        # Save uploaded file
        with open(file_path, "wb") as buffer:
            content = await photo.read()
            buffer.write(content)
        
        # Load image and extract face encoding
        image = face_recognition.load_image_file(str(file_path))
        face_encodings = face_recognition.face_encodings(image)
        
        if not face_encodings:
            # Delete the file if no face found
            os.remove(file_path)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No face detected in the image. Please upload a photo with a clear face."
            )
        
        # Use the first face encoding (if multiple faces, use the first one)
        face_encoding = face_encodings[0]
        
        # Convert numpy array to list for JSON serialization
        face_encoding_list = face_encoding.tolist()
        
        # Store both file path and encoding as JSON
        photo_data = {
            "file_path": str(file_path),
            "face_encoding": face_encoding_list
        }
        
        # Create user with photo data as JSON string
        new_user = models.User(photo=json.dumps(photo_data))
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        return new_user
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Clean up file on error
        if file_path.exists():
            os.remove(file_path)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing image: {str(e)}"
        )

@router.post("/login", response_model=schemas.Token)
def login(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user or not auth.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = auth.create_access_token({"sub": db_user.email})
    return {"access_token": token}