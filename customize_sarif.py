import json
import sys

def customize_sarif(input_file, output_file, findings):
    with open(input_file, 'r') as file:
        sarif_data = json.load(file)
    
    # Update SARIF to include finding IDs only
    for run in sarif_data.get("runs", []):
        for result in run.get("results", []):
            finding_id = findings.get(result.get("ruleId"))
            if finding_id:
                result["ruleId"] = str(finding_id)  # Replace ruleId with finding ID

    # Save modified SARIF data
    with open(output_file, 'w') as file:
        json.dump(sarif_data, file, indent=2)

if __name__ == "__main__":
    input_sarif = sys.argv[1]  # Input SARIF file
    output_sarif = sys.argv[2]  # Output SARIF file

    # Example findings mapping for demonstration
    findings = {
        "rule-id-1": "465",
        "rule-id-2": "123"
    }
    
    customize_sarif(input_sarif, output_sarif, findings)
