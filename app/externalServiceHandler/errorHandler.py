from fastapi.responses import JSONResponse

class ErrorHandler:
    @staticmethod
    def handle_database_error(error):
        return JSONResponse(content={"error": "Database error", "details": str(error)}, status_code=500)

    @staticmethod
    def handle_not_found(error):
        raise HTTPException(status_code=404, detail=error)

    @staticmethod
    def handle_validation_error(error):
        return JSONResponse(content={"error": "Validation error", "details": str(error)}, status_code=400)