# Data Schema

## `sample_attendance.csv`
This generated file contains dummy attendance records used to test the dashboard.

| Column Name      | Type    | Description                                             |
|------------------|---------|---------------------------------------------------------|
| `student_id`     | Integer | Matches ID in the SQLite `students` table.              |
| `date`           | String  | The date of the attendance record in YYYY-MM-DD format. |
| `timestamp`      | String  | Accurate timestamp of when attendance was captured.     |
| `subject`        | String  | Which subject/course this is marking attendance for.    |
| `marked_by`      | String  | Typically "System" indicating facial recognition.       |
| `confidence_score` | Float | The ML confidence %, usually between 62.0 and 99.0.     |
