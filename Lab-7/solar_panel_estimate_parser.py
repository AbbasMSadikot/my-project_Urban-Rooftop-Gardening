def clean_site_name(name):
    """
    Trims a site name, removes '#' and '@', and title-cases it.
    Assumes name is a non-empty string.
    """
    name = name.strip()
    for ch in ['#', '@']:
        name = name.replace(ch, '')
    return name.title()

def parse_monthly_units(text):
    """
    Converts a reading such as '320 kWh' into an int.
    Assumes only digits remain after removing 'kwh'.
    """
    return int(text.lower().replace('kwh', '').strip())

def panels_for_roof(text):
    """
    Works out how many 18 sq ft panels fit on a roof given as 'Lft x Wft'.
    Assumes text has two whole numbers separated by 'x'.
    """
    parts = text.lower().replace('ft', '').split('x')
    return int(parts[0]) * int(parts[1]) // 18

def main():
    print("==== Running clean_site_name ====")
    value = input("Enter the installation site name: ")
    print("Site name:", clean_site_name(value))

    print("\n==== Running parse_monthly_units ====")
    value = input("Enter monthly electricity use (e.g. 320 kWh): ")
    print("Monthly units:", parse_monthly_units(value))

    print("\n==== Running panels_for_roof ====")
    value = input("Enter roof size as LENGTHft x WIDTHft (e.g. 20ft x 15ft): ")
    print("Panels that fit:", panels_for_roof(value))

if __name__ == "__main__":
    main()
