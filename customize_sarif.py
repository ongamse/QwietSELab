import json
import sys

# Define a mapping from SARIF severities to GitHub SARIF levels
severity_to_level = {
    "critical": "error",
    "high": "error",
    "medium": "warning",
    "low": "note",
    "info": "note"
}

def customize_sarif(input_sarif, output_sarif, findings):
    with open(input_sarif, 'r') as file:
        sarif_data = json.load(file)

    for run in sarif_data.get("runs", []):
        for result in run.get("results", []):
            finding_id = result.get("ruleId")

            # Check if finding ID exists in findings
            if finding_id in findings:
                custom_severity = findings[finding_id]["severity"]
                result["level"] = severity_to_level.get(custom_severity, "error")
                
                # Prefix message with severity and alert ID
                alert_id = findings[finding_id]["id"]
                result["message"]["text"] = f"[{custom_severity.upper()}] Alert #{alert_id}: {result['message']['text']}"
            else:
                # Fallback to SARIF's own severity if no custom severity is available
                sarif_severity = result.get("severity", "info").lower()
                result["level"] = severity_to_level.get(sarif_severity, "note")
            
            # Log if severity does not match expected levels
            if "level" not in result:
                print(f"Warning: No level set for finding ID {finding_id}")

    with open(output_sarif, 'w') as file:
        json.dump(sarif_data, file, indent=2)

# Example findings dictionary (replace with actual findings data)
findings = {
    "finding-1": {"severity": "high", "id": "465"},
    "finding-2": {"severity": "critical", "id": "789"},
    # Add more finding IDs as needed
}

if __name__ == "__main__":
    input_sarif = sys.argv[1]
    output_sarif = sys.argv[2]
    customize_sarif(input_sarif, output_sarif, findings)
