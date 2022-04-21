import operator
import re

class Brain():

    def __init__(self, screen):

        self.screen = screen
        self.lastOperator = ''
        self.screenValue = ''
        self.operatorExists = False
        self.numberExists = False
        self.decimalExists = False

    def buttonPress(self, button):

        self.button = button
        self.screen.setStyleSheet('QLineEdit {color: rgb(0, 0, 0);}')
        self.screen.setMaxLength(100)

        if self.button == '/' or self.button == 'X' or self.button == '-' or self.button == '+':
            self.storeOperator()

        elif self.button == '.':
            self.decimal()

        elif self.button == '=':
            self.compute()

        elif self.button == '':
            self.button = 'C'
            self.clear()

        else:
            self.storeNumber()

    '''
    If numeric button presssed, add it to the screen value
    Do not store the number '0' if the previous button pressed was '/'
    '''
    def storeNumber(self):

        if len(self.screenValue) > 0:
            if self.screenValue[-1] == '/':
                if self.button == '0':
                    self.screen.setText(self.screenValue)
                    return
        
        self.screenValue += self.button
        self.screen.setText(self.screenValue)
        self.numberExists = True

    '''
    If operator button pressed, add it to the screen value
    Do not store the operator if no number has been entered
    If the previous button clicked was '.', add '0' before the operator
    If the previous button clicked was an operator, overwrite it
    '''
    def storeOperator(self):

        if len(self.screenValue) > 0:
            if self.numberExists == False:
                self.screenValue = self.screenValue[:-1]
                self.screenValue += self.button
            elif self.screenValue[-1] == '.':
                self.screenValue += '0'+self.button
            elif self.screenValue == '/' or self.screenValue == 'X' or self.screenValue == '-' or self.screenValue == '+':
                self.screenValue = self.screenValue[:-1]
                self.screenValue += self.button
            else:
                self.screenValue += self.button

            self.screen.setText(self.screenValue)
            self.lastOperator = self.button
            self.operatorExists = True
            self.decimalExists = False
            self.numberExists = False
        else:
            self.screen.setText(self.screenValue)

    '''
    If decimal button pressed, add it to the screen value
    If there is already a decimal in the number, skip
    If There is no number before the decimal, add a '0' before
    '''
    def decimal(self):

        if self.decimalExists == True:
            self.screen.setText(self.screenValue)
        else:
            if self.numberExists == False:
                self.screenValue += '0'+self.button
                self.screen.setText(self.screenValue)
            else:
                self.screenValue += self.button
                self.screen.setText(self.screenValue)      
            
            self.decimalExists = True

    '''
    If compute button pressed, convert string screenValue to a numbers list and an operators list
    If the last value in the screenValue is an operator, remove it
    Parse through each list one at a time to calculate. This will ignore operator priority
    '''
    def compute(self):

        if self.screenValue[-1] == '/' or self.screenValue[-1] == 'X' or self.screenValue[-1] == '-' or self.screenValue[-1] == '+' or self.screenValue[-1] == '.':
            self.screenValue = self.screenValue[:-1]

        numbersList = re.findall(r"[-+]?\d*\.\d+|\d+", self.screenValue)
        floatList = [float(x) for x in numbersList]
        operatorsString = re.sub('[0123456789.]', '', self.screenValue)
        operatorsList = list(operatorsString)

        ops = { "+": operator.add, "-": operator.sub, 'X': operator.mul, '/': operator.truediv}

        result = floatList[0]
        for i in range(1, len(floatList)):
            if operatorsList[i - 1] in ops:
                result = ops[operatorsList[i - 1]](result, floatList[i])

        final = str(result)

        self.screen.setMaxLength(13)
        self.screen.setText(final)
        self.screen.setStyleSheet('QLineEdit {color: rgb(50, 205, 50);}')
        self.operatorExists = False
        self.numberExists = True

    def clear(self):
        self.screen.setText('')
        self.lastOperator = ''
        self.screenValue = ''
        self.operatorExists = False
        self.decimalExists = False
        self.numberExists = False