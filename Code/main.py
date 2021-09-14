#########################################################################
# CODECADEMY PORTFOLIO PROJECT:     U.S. Medical Insurance Costs       #
# AUTHOR:                           Jonas Bauer, M.Sc                 #
# GITHUB:                           https://github.com/jonasbauer192 #
# DISCORD:                          hUXEL#0258                      #
# LOCATION / TIME ZONE:             Munich, Germany / UTC+01:00    #
###################################################################

import csv

class Patients:

    def __init__(self):
        self.averageAttributes = {}
        self.countingAttributes = {}
        self.BMIaverageCostDict = {}
        self.smokerAverageCosts = {}

    def convertDataMethod(self, file):
        # converts teh data into a dict
        with open(file) as insuranceFile:
            insuranceReader = csv.DictReader(insuranceFile)
            patientsDict = {}
            for count, row in enumerate(insuranceReader):
                # create a dict for each row if the csv file
                rowDict = {"Age": int(row["age"]),
                           "Sex": row["sex"],
                           "BMI": float(row["bmi"]),
                           "Children": int(row["children"]),
                           "Smoker": row["smoker"],
                           "Region": row["region"],
                           "Charges": float(row["charges"])}
                patientsDict.update({count: rowDict})
        # set patientDict as class attribute
        self.patientsDict = patientsDict

    def averageAttributesMethod(self, attribute):
        # determines the average of the provided attributes
        attributeSum = 0
        for counter, patientData in enumerate(self.patientsDict.values()):
            attributeSum += patientData[attribute]
        average = attributeSum / (counter + 1)
        self.averageAttributes[attribute] = average

    def countingAttributesMethod(self, attribute):
        # counts how often which attribute occures
        attributesDict = {}
        for patientData in self.patientsDict.values():
            valueSafed = attributesDict.pop(patientData[attribute], 0)
            valueSafed += 1
            attributesDict[patientData[attribute]] = valueSafed
        self.countingAttributes[attribute] = attributesDict

    def BMIvsCostsMethod(self):
        # average charges for each BMI category
        BMIscale = {'Underweight': 18.4,
                    'Healthy Weight': 24.9,
                    'Overweight': 29.9,
                    'Obesity': 1000}
        BMIcostDict = {}
        for patientData in self.patientsDict.values():
            for key, value in BMIscale.items():
                if patientData["BMI"] <= value:
                    # remove and store the value (= subDict) of the regarded category
                    storedSubDict = BMIcostDict.pop(key, {})
                    # remove and store the values of the keys
                    totalChargesStored = storedSubDict.pop("Total Charges", 0)
                    totalNumberStored = storedSubDict.pop("Total Number", 0)
                    # update the stored values
                    totalChargesStored += patientData["Charges"]
                    totalNumberStored += 1
                    # return the updated values back into the subDict and return this subDict to the BMIcostDict
                    storedSubDict.update({"Total Charges": totalChargesStored, "Total Number": totalNumberStored})
                    BMIcostDict[key] = storedSubDict
                    break
        # determine average costs for each category
        for key, subDict in BMIcostDict.items():
            average = subDict["Total Charges"] / subDict["Total Number"]
            self.BMIaverageCostDict['Average charge for patients with ' + key] = average

    def smokerVsNonsmokerMethod(self):
        # average charges smoker vs. non-smoker
        totalDict = {}
        for subDict in self.patientsDict.values():
            for status, title in {'yes': 'Smoker', 'no': 'Non Smoker'}.items():
                if subDict["Smoker"] == status:
                    storageDict = totalDict.pop(title, {})
                    totalChargeStored = storageDict.pop("Total Charge", 0)
                    totalNumberStored = storageDict.pop("Total Number", 0)
                    totalChargeStored += subDict["Charges"]
                    totalNumberStored += 1
                    storageDict.update({"Total Charge": totalChargeStored, "Total Number": totalNumberStored})
                    totalDict[title] = storageDict
        # determine average costs for smoker and non-smoker
        for key, subDict in totalDict.items():
            self.smokerAverageCosts[key] = subDict["Total Charge"] / subDict["Total Number"]

    def averageAgeForChildrenMethod(self):
        # average age for all patients having at least one child
        sum = 0
        counter = 0
        for subDict in self.patientsDict.values():
            if subDict["Children"] >= 1:
                sum += subDict["Age"]
                counter += 1
        self.averageAgeForChildren = sum / counter

    def findChargesForExtremumMethod(self, attribute):

        # PART 1: Find the maximum value of the provided attribute
        attributeList = []
        for subDict in self.patientsDict.values():
            attributeList.append(subDict[attribute])
        maximum = max(attributeList)

        # PART 2: find (average) charges for the maximum value found
        chargesOfMaximum = []
        for key, subDict in self.patientsDict.items():
            if subDict[attribute] == maximum:
                chargesOfMaximum.append(subDict["Charges"])
        average = sum(chargesOfMaximum) / len(chargesOfMaximum)
        if attribute == "Age":
            self.chargesForMaxAge = average
        elif attribute == "BMI":
            self.chargesForMaxBMI = average

file = 'insurance.csv'
patients = Patients()
patients.convertDataMethod(file)
# perform evaluation of the averages
averagesToDetermine = ["Age", "BMI", "Children", "Charges"]
for attribute in averagesToDetermine:
    patients.averageAttributesMethod(attribute)

majoritiesToDetermine = ["Sex", "Smoker", "Region"]
for attribute in majoritiesToDetermine:
    patients.countingAttributesMethod(attribute)

patients.BMIvsCostsMethod()
patients.smokerVsNonsmokerMethod()
patients.averageAgeForChildrenMethod()
patients.findChargesForExtremumMethod("Age")
patients.findChargesForExtremumMethod("BMI")




