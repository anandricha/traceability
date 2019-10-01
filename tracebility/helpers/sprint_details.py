from tracebility.database import DB

class traceability_data:
    def sprint_details(self,sprint):
        # print(sprint)
        query = {'Sprint': sprint}
        data = DB.find('data',query)
        print("complete data---------- ",data)
        sprint_sheet_data = list()
        for items in data:
            x=0
            if x==0:
                headers = list(items)
                headers = headers[2:]
                print("this is header data", headers[2:])
                x=+1
            sprint_values = list(items.values())
            sprint_sheet_data.append(sprint_values[2:])
            print( sprint+"complete data ",sprint_sheet_data)
        return [headers,sprint_sheet_data]
