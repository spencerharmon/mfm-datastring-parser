from .exceptions import DataMemberDataError
import re


class DataMemberData(object):
    def __init__(self, data_string):
        self.data_string = data_string
        if self.data_string == '':
            self.empty = True
            self.char_list = []
            self.max_index = 0
            self.truncated = False
            self.data = None
            self.strlen = 0
        else:
            self.char_list = [char for char in self.data_string]
            self.max_index = len(self.char_list) - 1
            self.truncated = self.detect_trunc()
            self.data, self.strlen = self.recursive_parse(self.char_list)
#        if self.strlen != self.max_index:
#            raise DataMemberDataError(f'Received {len(char_list)} characters, but processed {self.strlen}.')

    def __dict__(self):
        return self.data
    
    def recursive_parse(self, char_list, i=0):
        ret = {}
        # begin with left-hand-side string
        lhs = True
        lhs_chars = []
        rhs_chars = []
        rhs_dict = {}
        rhs_list = []
        while i <= self.max_index:
            char = char_list[i]
            # ignore
            if char == "(":
                i += 1
                continue


            elif char == "=":
                # a string like `something=(etc` indicates that data member `something` contains an instance of a class containing
                # data members. So, we'll split the char_list and run the thing from this parenthesis.
                if char_list[i+1] == "(":
                    rhs_dict, new_i = self.recursive_parse(char_list, i+1)
                    #hacky. decrement one to counter extraneous increment.
                    i = new_i - 1
                # help! it's a list!
                elif char_list[i+1] == "[":
                    rhs_list, new_i = self.parse_list(char_list, i+1)
                    i = new_i - 1
                lhs = False
                i += 1
                continue

            elif char == ")" or char == "," or (self.truncated and char == "X"):
                datamember_name = ''.join(lhs_chars)
                if rhs_chars != []:
                    ret[datamember_name] = ''.join(rhs_chars)
                elif rhs_dict != {}:
                    ret[datamember_name] = rhs_dict
                elif rhs_list != []:
                    ret[datamember_name] = rhs_list
                lhs_chars = []
                rhs_chars = []
                rhs_dict = {}
                rhs_list = []
                i += 1
                # consider ourselves done when we reach a close paren. This allows the function to recurse.
                if char == ")" or char == "X":
                    return ret, i
                elif char == ",":
                    lhs = True
                    continue

            # only append if none of the above returned or continued.
            if lhs:
                lhs_chars.append(char)
            else:
                rhs_chars.append(char)
                
            i += 1


        # should have returned by now no matter what. Consider invalid and raise an error.
        raise DataMemberDataError("Data string parsing ended before data returned.")

    def detect_trunc(self):
        if self.char_list[self.max_index] == "X":
            return True
        else:
            return False

    def parse_list(self, char_list, i):
        """
        parse_list is executed by recursive_parse when it encounters a list.
        list format in a data string is:
           (datamember_name=[1]=val,[2]=val,nextdatamamber=etc)
        index (i) passed to parse_list is the first "["
        so, extract the vals from in between the "]" and the ",", and stop when we reach the next datamember
        also, be careful to return something even if the data string is truncated with an "X" within this list.
        :param: char_string = list of chars in atom string data
        :param: i = index on which the list begins
        :return: dm_list = the list of values for the data member we're parsing
        :return: i = the index of the first character of the next data member
        """
        dm_list = []
        list_item = []
        lhs = True
        while i <= self.max_index:
            char = char_list[i]

            if char == "=":
                lhs = False
            # lists in the data string can end with a ',', an 'X', or a ')'
            elif char == ",":
                # new list item
                if char_list[i+1] == "[":
                    lhs = True
                    dm_list.append(''.join(list_item))
                    list_item = []
                    i += 1
                    continue
                else:
                    # list is over. return what we have.
                    return dm_list, i
            elif char == ")":
                # end of data_string is also end of list.
                dm_list.append(''.join(list_item))
                return dm_list, i
            # the truncated case
            elif char == "X" and i == self.max_index and self.truncated:
                return dm_list, i
            else:
                if not lhs:
                    list_item.append(char)

            i += 1

        return dm_list, i
