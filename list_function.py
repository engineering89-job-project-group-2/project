from flask_table import Table, Col


# Declare your table
class ItemTable(Table):
    job = Col('Job Title')
    rank = Col('Rank')
    salary = Col('Salary')


# Get some objects
class Item(object):
    def __init__(self, job, rank, salary):
        self.job = job
        self.rank = rank
        self.salary = salary


def display_table_rank(list):
    # takes individual entries from df and assigns to table columns/rows
    items = [Item(list['Job Title'][0], list['Rank'][0], list['Salary'][0]),
             Item(list['Job Title'][1], list['Rank'][1], list['Salary'][1]),
             Item(list['Job Title'][2], list['Rank'][2], list['Salary'][2])]
    table = ItemTable(items) # creates table

    # return the table in html format
    return table.__html__()