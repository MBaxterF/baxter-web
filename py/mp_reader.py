import openpyxl
import pandas

from marking_plan import MarkingPlan


class MPReader:
    def __init__(self):
        self.__marking_plan = None

    def __read(self, excel):
        sheets = openpyxl.load_workbook(excel)
        sheet = sheets['Spécifications techniques']

        plan = [[], [], [], [], [], []]

        i = 0

        while sheet['E' + str(i + 12)].value is not None:
            plan[1].append(sheet['B' + str(i + 12)].value)
            plan[2].append(sheet['C' + str(i + 12)].value)
            plan[3].append(sheet['D' + str(i + 12)].value)
            plan[0].append(sheet['E' + str(i + 12)].value)
            plan[4].append(sheet['F' + str(i + 12)].value)

            i += 1

        return plan

    def build(self, excel):
        self.__marking_plan = MarkingPlan()
        plan = self.__read(excel)

        for i in range(len(plan[0])):
            self.__marking_plan.put((plan[0][i], plan[1][i], plan[2][i], plan[3][i],
                                     plan[4][i]))

    def render(self):
        return self.__marking_plan
