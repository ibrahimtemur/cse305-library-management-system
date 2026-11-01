# Name(s) Surname(s) : Ibrahim Temur, Omer Faruk Kuş
# Student No(s)#: 231805033, 231805026
# General Comments: Utility to parse Mermaid domain model diagram and output exact counts of classes, attributes, enums, and associations.

import re
import sys

def parse_mmd(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    classes = {}
    enums = {}
    current_class = None
    is_enum = False

    for line in lines:
        line = line.strip()
        m_class = re.match(r"^class\s+(\w+)\s*\{", line)
        if m_class:
            current_class = m_class.group(1)
            classes[current_class] = []
            is_enum = False
            continue
        if line == "}":
            current_class = None
            is_enum = False
            continue
        if current_class:
            if line == "<<enumeration>>":
                is_enum = True
                enums[current_class] = []
                del classes[current_class]
                continue
            if is_enum:
                enums[current_class].append(line)
            else:
                classes[current_class].append(line)

    associations = []
    for line in lines:
        line = line.strip()
        m_assoc = re.match(r'^(\w+)\s+"([^"]+)"\s+--\s+"([^"]+)"\s+(\w+)\s*:\s*(.*)$', line)
        if m_assoc:
            associations.append(m_assoc.groups())

    print("=== CLASSES & ATTRIBUTES ===")
    total_attrs = 0
    for cls, attrs in classes.items():
        print(f"{cls} ({len(attrs)} attributes):")
        for a in attrs:
            print(f"  - {a}")
        total_attrs += len(attrs)
    print(f"Total Classes: {len(classes)}")
    print(f"Total Attributes: {total_attrs}")

    print("\n=== ENUMERATIONS & VALUES ===")
    total_enum_vals = 0
    for enm, vals in enums.items():
        print(f"{enm} ({len(vals)} values):")
        for v in vals:
            print(f"  - {v}")
        total_enum_vals += len(vals)
    print(f"Total Enumerations: {len(enums)}")
    print(f"Total Enum Values: {total_enum_vals}")

    print("\n=== ASSOCIATIONS ===")
    for i, a in enumerate(associations, 1):
        print(f"A{i}: {a[0]} \"{a[1]}\" -- \"{a[2]}\" {a[3]} : {a[4]}")
    print(f"Total Associations: {len(associations)}")

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "docs/01-proposal/images/domain-model.mmd"
    parse_mmd(path)
