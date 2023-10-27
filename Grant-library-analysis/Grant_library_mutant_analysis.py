#This script performs the data manipulation and counts that ultimately becomes the data that is used
#for the confusion matrix.


import os

# Create a directory for output files
output_folder = "GrantLibrary_HCD_output_files"
if not os.path.exists(output_folder):
    os.mkdir(output_folder)

def write_to_file(output_file, data):
    with open(output_file, 'w', encoding='latin-1') as output:
        output.writelines(data)

# Task 1: Compare Plate_indices.txt with LCD_locked_search.txt
plate_indices_file = "Plate_indices.txt"
lcd_locked_search_file = "LCD_locked_search.txt"
output_file_task1 = os.path.join(output_folder, "Mekalanos_empty_wells.txt")

lcd_locked_search_set = set(line.strip().split('\t')[0] for line in open(lcd_locked_search_file, 'r', encoding='latin-1'))
non_matching_rows = []
header = None

with open(plate_indices_file, 'r', encoding='latin-1') as plate_indices:
    for line in plate_indices:
        if header is None:
            header = line
        columns = line.strip().split('\t')
        if columns and columns[0] not in lcd_locked_search_set:
            non_matching_rows.append(line)

write_to_file(output_file_task1, [header] + non_matching_rows)
num_entries_task1 = len(non_matching_rows)
print(f"Task 1 Done! Entries from Plate_indices.txt that shouldn't match LCD_locked_search.txt have been written to 'Mekalanos_empty_wells.txt'.")
print(f"Number of entries that met the condition in Task 1: {num_entries_task1}")

# Task 2: Compare 'Mekalanos_empty_wells.txt' with 'Observed_negatives.txt'
output_file_task2 = output_file_task1
observed_negatives_file = "Observed_negatives.txt"
comparison_output_file = os.path.join(output_folder, "true_negatives.txt")
non_matching_output_file = os.path.join(output_folder, "false_positives.txt")

shouldnt_match_rows = open(output_file_task2, 'r', encoding='latin-1').readlines()
observed_negatives_set = set(line.strip().split('\t')[0] for line in open(observed_negatives_file, 'r', encoding='latin-1'))

non_matching_rows = [shouldnt_match_rows[0]] + [row for row in shouldnt_match_rows[1:] if row.strip().split('\t')[0] not in observed_negatives_set]
write_to_file(non_matching_output_file, non_matching_rows)

matching_rows = [row for row in shouldnt_match_rows if row.strip().split('\t')[0] in observed_negatives_set]
write_to_file(comparison_output_file, matching_rows)

num_entries_task2_matching = len(matching_rows) - 1
num_entries_task2_non_matching = len(non_matching_rows) - 1
print("Task 2 Done! Matching entries (with headers) have been written to 'true_negatives.txt', and non-matching entries (with headers) have been written to 'false_positives.txt'.")
print(f"Number of entries that met the condition in Task 2 (Matching): {num_entries_task2_matching}")
print(f"Number of entries that met the condition in Task 2 (Non-Matching): {num_entries_task2_non_matching}")

# Task 3: Find Duplicate Entries in LCD_locked_search.txt
mek_mut_list_file_task3 = "LCD_locked_search.txt"
output_file_task3 = os.path.join(output_folder, "duplicate_Mekalanos_mutants.txt")

header = None
mek_mut_list_entries = {}
duplicate_entries = []

with open(mek_mut_list_file_task3, 'r', encoding='latin-1') as mek_mut_list:
    header = next(mek_mut_list)
    for line in mek_mut_list:
        columns = line.strip().split('\t')
        if columns:
            entry = columns[0]
            if entry in mek_mut_list_entries:
                duplicate_entries.append(line)
            else:
                mek_mut_list_entries[entry] = True

write_to_file(output_file_task3, [header] + duplicate_entries)
num_duplicate_entries = len(duplicate_entries)
print(f"Task 3 Done! Found {num_duplicate_entries} duplicate entries in LCD_locked_search.txt and wrote them to 'duplicate_Mekalanos_mutants.txt'.")

# Task 4: Find Unique Entries in Mekalanos_mutants.txt that should match Plate_indices.txt
plate_indices_file_task4 = "Plate_indices.txt"
mekalanos_mutants_file_task4 = "LCD_locked_search.txt"
output_file_task4 = os.path.join(output_folder, "unique_Mekalanos_mutants.txt")

plate_indices_set_task4 = set(line.strip().split('\t')[0] for line in open(plate_indices_file_task4, 'r', encoding='latin-1'))
matching_rows_task4 = []
header_task4 = None
seen_entries_task4 = set()

with open(mekalanos_mutants_file_task4, 'r', encoding='latin-1') as mekalanos_mutants_task4:
    for line in mekalanos_mutants_task4:
        if header_task4 is None:
            header_task4 = line
        else:
            columns = line.strip().split('\t')
            if columns:
                entry = columns[0]
                if entry in plate_indices_set_task4 and entry not in seen_entries_task4:
                    matching_rows_task4.append(line)
                    seen_entries_task4.add(entry)
# Task 4: Find Unique Entries in Mekalanos_mutants.txt that should match Plate_indices.txt
write_to_file(output_file_task4, [header_task4] + matching_rows_task4)
num_entries_matched_task4 = len(matching_rows_task4)
print(f"Task 4 Done! {num_entries_matched_task4} unique entries from Mekalanos_mutants.txt that should match Plate_indices.txt have been written to 'unique_Mekalanos_mutants.txt'.")

# Task 5: Compare 'Observed_false_negatives.txt' with 'unique_Mekalanos_mutants.txt'
# Define the filenames
observed_false_negatives_file = "Observed_false_negatives.txt"  # Define the path to your Observed_false_negatives.txt file
output_file_task5 = os.path.join(output_folder, "Grant_Library_Mutants.txt")

# Read the first column from Observed_false_negatives.txt into a set
observed_false_negatives_set = set()
with open(observed_false_negatives_file, 'r', encoding='latin-1') as observed_false_negatives:
    for line in observed_false_negatives:
        columns = line.strip().split('\t')
        if columns:  # Ensure there's at least one column
            observed_false_negatives_set.add(columns[0])

# Create a set to store unique entries from unique_Mekalanos_mutants.txt
unique_entries = set()
header_task5 = None  # To store the header

with open(os.path.join(output_folder, "unique_Mekalanos_mutants.txt"), 'r', encoding='latin-1') as unique_mekalanos_mutants_task5:
    for line in unique_mekalanos_mutants_task5:
        columns = line.strip().split('\t')
        if not header_task5:
            header_task5 = line  # Store the header
        elif columns:  # Ensure there's at least one column
            entry = columns[0]  # Extract the entry from the first column
            if entry not in observed_false_negatives_set:
                unique_entries.add(line)

# Write the new file with the header to Grant_Library_Mutants.txt
with open(output_file_task5, 'w', encoding='latin-1') as output_task5:
    output_task5.write(header_task5)  # Write the header
    output_task5.writelines(unique_entries)

num_entries_task5 = len(unique_entries)  # Count of unique entries in the new file
print(f"Task 5 Done! Unique entries from unique_Mekalanos_mutants.txt (excluding those matching Observed_false_negatives.txt) have been written to 'Grant_Library_Mutants.txt'.")
print(f"Number of unique entries in the new file: {num_entries_task5}")

#Task six

# Calculate the number of entries in Observed_false_negatives.txt
observed_false_negatives_file = "Observed_false_negatives.txt"  # Define the path to your Observed_false_negatives.txt file
num_entries_observed_false_negatives = 0

with open(observed_false_negatives_file, 'r', encoding='latin-1') as observed_false_negatives:
    header = next(observed_false_negatives)  # Read the header
    for line in observed_false_negatives:
        num_entries_observed_false_negatives += 1

# Task 6: Calculate and print Confusion Matrix inputs
# Define variables
X = num_entries_task5
Y = num_entries_task2_matching
A = num_entries_observed_false_negatives
B = num_entries_task2_non_matching

# Format the output as a single string with red text
confusion_matrix_inputs = (
    f"Confusion matrix inputs:\n"
    f"\033[91mTrue Positives = {X}\n"
    f"\033[91mTrue Negatives = {Y}\n"
    f"\033[91mFalse Positives = {A}\n"
    f"\033[91mFalse Negatives = {B}\033[0m"
)

# Print the formatted confusion matrix inputs
print(confusion_matrix_inputs)

# Confusion matrix output

# Given values from previous tasks
TP = num_entries_task5
TN = num_entries_task2_matching
FP = num_entries_observed_false_negatives
FN = num_entries_task2_non_matching
P = TP + FN  # Total positives
N = TN + FP  # Total negatives

# Sensitivity (True Positive Rate)
TPR = TP / (TP + FN)

# Specificity (True Negative Rate)
SPC = TN / (FP + TN)

# Precision (Positive Predictive Value)
PPV = TP / (TP + FP)

# Negative Predictive Value
NPV = TN / (TN + FN)

# False Positive Rate
FPR = FP / (FP + TN)

# False Discovery Rate
FDR = FP / (FP + TP)

# False Negative Rate
FNR = FN / (FN + TP)

# Accuracy
ACC = (TP + TN) / (P + N)

# F1 Score (Recall)
F1 = 2 * TP / (2 * TP + FP + FN)

# Matthews Correlation Coefficient
MCC = (TP * TN - FP * FN) / ((TP + FP) * (TP + FN) * (TN + FP) * (TN + FN))**0.5

# Print Confusion matrix outputs in red
confusion_matrix_outputs = (
    f"Confusion matrix outputs:\n"
    f"\033[91mSensitivity (True Positive Rate): {TPR:.4f}\033[0m\n"
    f"\033[91mSpecificity (True Negative Rate): {SPC:.4f}\033[0m\n"
    f"\033[91mPrecision (Positive Predictive Value): {PPV:.4f}\033[0m\n"
    f"\033[91mNegative Predictive Value: {NPV:.4f}\033[0m\n"
    f"\033[91mFalse Positive Rate: {FPR:.4f}\033[0m\n"
    f"\033[91mFalse Discovery Rate: {FDR:.4f}\033[0m\n"
    f"\033[91mFalse Negative Rate: {FNR:.4f}\033[0m\n"
    f"\033[91mAccuracy: {ACC:.4f}\033[0m\n"
    f"\033[91mRecall (F1 Score): {F1:.4f}\033[0m\n"
    f"\033[91mMatthews Correlation Coefficient: {MCC:.4f}\033[0m"
)

print(confusion_matrix_outputs)




