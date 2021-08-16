def compare_alert_rules(src_ar: list, dst_ar: list):
    new_ar = []
    # loops through src_ar (source tenant) to find the missing alert rules
    for item in src_ar:
        # skips alert rule named 'Default Alert Rule'
        if item['name'] == 'Default Alert Rule' in [key['name'] for key in dst_ar]:
            continue
        #check if the key 'name' is in both tenants. If not, appends the missing alert rule to a new list
        if item['scanConfigType'] == 'STANDARD':
            if item['name'] not in [key['name'] for key in dst_ar]:
                # prints the value of key 'policyScanConfigId' and 'name' of the missing value
                # appends the missing values from src_ar
                new_ar.append(item)
    return new_ar