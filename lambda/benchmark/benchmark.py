import os
import json
import xlsxwriter  # Ensure you have installed this library: pip install xlsxwriter

def optimal(EditedFields, fields_to_fill, optimal_output_path, benchmark_path):   
    # Load the optimal output for comparison
    with open(optimal_output_path, "r", encoding="utf-8") as f:
        optimal_output = json.load(f)

    # Initialize benchmark metrics
    total_fields = len(fields_to_fill)
    correctly_filled = 0
    incorrectly_filled = 0
    missed_fields = 0

    # Compare EditedFields with optimalOutput
    for field_name in fields_to_fill:
        optimal_value = optimal_output.get(field_name, None)
        edited_value = EditedFields.get(field_name, None)

        if edited_value == optimal_value:
            correctly_filled += 1
        elif edited_value is not None:
            incorrectly_filled += 1
        else:
            missed_fields += 1

    # Add fields filled incorrectly that were not in optimalOutput
    extra_fields = set(EditedFields.keys()) - set(optimal_output.keys())
    incorrectly_filled += len(extra_fields)

    # Save benchmark results to an XLSX file
    workbook = xlsxwriter.Workbook(benchmark_path)
    worksheet = workbook.add_worksheet()

    # Write headers
    worksheet.write(0, 0, "Model")
    worksheet.write(0, 1, "Total Fields")
    worksheet.write(0, 2, "Correctly Filled")
    worksheet.write(0, 3, "Incorrectly Filled")
    worksheet.write(0, 4, "Missed Fields")

    # Write data for the current model
    worksheet.write(1, 0, "meta-llama/llama-4-maverick-17b-128e-instruct")  # Model name
    worksheet.write(1, 1, total_fields)
    worksheet.write(1, 2, correctly_filled)
    worksheet.write(1, 3, incorrectly_filled)
    worksheet.write(1, 4, missed_fields)

    workbook.close()

    print(f"\nBenchmark results saved to:\n{os.path.abspath(benchmark_path)}")