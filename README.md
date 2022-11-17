## File Storage Backend made using Fast API

**To run this app, type the following commands on your terminal:**

1. `git clone https://github.com/ayushrajdahal/videoapp`
2. `cd videoapp`
3. `pip install -r requirements.txt`.
4. `python3 main.py` or `uvicorn main:app --reload`

**API Endpoints:**

1. `/upload-video` recieves and validates the video file

2. `/list-videos` lists videos being uploaded after applying these optional filters:
    - **minLength:** minimum video length in seconds
    - **maxLength:** maximum video length in seconds
    - **dateFrom:** earliest date in 'YYYY-MM-DD'
    - **dateTill:** latest date in 'YYYY-MM-DD'

3. `/calculate-charges` calculates total charge, given the video size, length, and file type via Query Parameters

4. `/stream-video` streams stored video, given the filename as an input (both with and without the file extension)

To access the API Documentation page, go to http://127.0.0.1:5000/docs