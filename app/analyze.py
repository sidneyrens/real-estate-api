import re

def analyze_recommendations(text):
    recommendations = []

    # Example Regex to find actionable items; this will need to be tailored
    # based on how recommendations are formatted in the reports
    pattern = re.compile(r'(?i)(repair|replace|fix|check|service).*?\.')
    matches = pattern.findall(text)

    # Group recommendations if necessary (simple in this case)
    for match in matches:
        recommendations.append(match.strip())

    return {"recommendations": recommendations}
