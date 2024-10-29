import json
import sys

# Define mappings for severity customization and the findings data (mock example).
severity_mapping = {
    "error": "high",  # Or "critical" if applicable
    # Add mappings for other severity levels if needed
}

def customize_sarif(input_sarif_path, output_sarif_path, findings_data):
    with open(input_sarif_path, 'r') as file:
        sarif_data = json.load(file)

    # Loop through results to update severities and IDs
    for run in sarif_data.get("runs", []):
        for result in run.get("results", []):
            # Map severity level
            sarif_severity = result["level"]
            custom_severity = severity_mapping.get(sarif_severity, sarif_severity)
            result["level"] = custom_severity
            
            # Map finding ID to alert number
            finding_id = findings_data.get(result.get("ruleId"))
            if finding_id:
                result["ruleId"] = finding_id

    with open(output_sarif_path, 'w') as file:
        json.dump(sarif_data, file, indent=2)
    print(f"SARIF customization complete. Output saved to {output_sarif_path}")

# Usage
if __name__ == "__main__":
    input_sarif = sys.argv[1]
    output_sarif = sys.argv[2]
    findings = {
        "alert-1": "finding-001",
        "alert-2": "finding-002"
        # Populate findings with actual ruleId and finding ID mappings
    }
    customize_sarif(input_sarif, output_sarif, findings)
