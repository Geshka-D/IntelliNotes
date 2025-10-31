# API Endpoints

All routes are exposed under the /api prefix.

## Notes

- GET /api/notes – list stored notes with summaries
- GET /api/notes/{note_id} – detailed note (summary, transcript, metadata)
- DELETE /api/notes/{note_id} – remove a stored note

## Lecture ingestion

- POST /api/lectures/upload – multipart upload (ile, optional 	itle)
- POST /api/lectures/text – JSON body { "text": "...", "title": "optional" }
- POST /api/lectures/process-recording – JSON body { "filename": "...", "title": "optional" }

## Recording control

- POST /api/recording/start
- POST /api/recording/stop
- GET /api/recording/status
- GET /api/recording/list
- GET /api/recording/{filename} – download
- GET /api/recording/{filename}/stream – stream audio
- DELETE /api/recording/{filename} – delete file
