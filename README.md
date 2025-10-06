# GPA Calculator

## Overview

A powerful GPA calculator that not only calculates your current GPA but also provides insights and recommendations for improvement. The tool analyzes your grades, identifies courses that need attention, and projects potential GPA improvements.

## Features

- Calculate current GPA based on a standard 4.0 scale
- Identify courses that must be retaken (failing grades)
- Get recommendations for courses that could improve your GPA if retaken
- View potential GPA improvements based on different retake scenarios
- Simple text-based input file format
- Support for various grade types (A, A-, B+, etc.)

## Requirements

- Python 3.x (No additional packages required)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/wkdkavishka/gpa-calculator.git
   cd gpa-calculator
   ```

## How to Use

### 1. Prepare Your Results File

Create a text file (e.g., `results.txt`) with your course information in the following format:

```
COURSE_CODE,CREDITS,GRADE
```

Example:

```
SCS1201,3,B-
SCS1202,3,A
SCS1203,3,B+
```

### 2. Run the Calculator

Execute the script with your results file as an argument:

```bash
python gpa_calculator.py results.txt
```

### 3. Review the Output

The tool will display:

- Your current GPA
- Potential GPA after retaking failed courses
- Potential GPA after retaking both failed and recommended courses
- List of courses that must be retaken (failing grades)
- Recommendations for courses that could improve your GPA if retaken

### Supported Grades

The calculator supports the following grade formats:

- A, A-, B+, B, B-, C+, C, C-, D+, D, E, F
- Special cases: WH (Withheld), NC (Not Completed), CM (Completed Module)

## Example

Given the sample `results.txt` file, the output will show:

- Current GPA calculation
- Courses that need to be retaken (F, E, WH grades)
- Recommended retakes (D and D+ grades)
- Potential GPA improvements

## License

This project is free to use for any purpose. No attribution is required.

## Contributing

Contributions are welcome! If you'd like to contribute, please:

1. Fork the repository
2. Create a new branch for your feature
3. Submit a pull request

## Support

For any issues or feature requests, please open an issue on the [GitHub repository](https://github.com/wkdkavishka/gpa-calculator).
