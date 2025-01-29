import sys

# Grade points mapping
grade_points = {
    "A": 4.0,
    "B+": 3.5,
    "B": 3.0,
    "C+": 2.5,
    "C": 2.0,
    "D+": 1.5,
    "D": 1.0,
    "F": 0.0,
    "E": 0.0
}

def parse_courses(file_path):
    """Parse the courses file into a list of dictionaries."""
    courses = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                # Split by comma and trim whitespace
                code, credits, result = line.strip().split(',')
                courses.append({
                    "code": code,
                    "credits": int(credits),
                    "result": result
                })
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)
    return courses

def calculate_gpa(courses):
    """Calculate GPA from a list of courses."""
    total_grade_points = 0
    total_credits = 0

    for course in courses:
        credits = course["credits"]
        result = course["result"]
        grade_point = grade_points.get(result, 0)  # Default to 0 for failed courses
        total_grade_points += credits * grade_point
        total_credits += credits

    # Avoid division by zero
    return total_grade_points / total_credits if total_credits > 0 else 0

if __name__ == "__main__":
    # Check if a file path is provided as an argument
    if len(sys.argv) != 2:
        print("Usage: python gpa_calculator.py <courses_file>")
        sys.exit(1)

    file_path = sys.argv[1]
    courses = parse_courses(file_path)
    gpa = calculate_gpa(courses)
    print(f"Your GPA is: {gpa:.2f}")
