from pydantic import BaseModel, Field


class PredictionResponse(BaseModel):
    """
    Schema for cancer prediction API response
    """

    status: str = Field(
        ...,
        example="success",
        description="Status of the API request"
    )

    file_type: str = Field(
        ...,
        example="pdf",
        description="Uploaded file type"
    )

    images_processed: int = Field(
        ...,
        example=3,
        description="Number of images analyzed by the CNN"
    )

    prediction: str = Field(
        ...,
        example="Cancer Detected",
        description="Final prediction result"
    )

    confidence: float = Field(
        ...,
        example=0.87,
        description="Confidence score of the prediction"
    )
