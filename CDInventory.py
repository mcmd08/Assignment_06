#------------------------------------------#
# Title: Assignment06.py
# Desc: Working with classes and functions.
# Change Log: (Who, When, What)
# Maria Dacutanan, 2020-Aug-16, Updated read_file function to include error handling for file not existing
# Maria Dacutanan, 2020-Aug-16, Updated show_inventory function to include Check for empty table
# Maria Dacutanan, 2020-Aug-16, Added get_newInventory function in class IO
# Maria Dacutanan, 2020-Aug-16, Added add_newInventory function in class DataProcessor
# Maria Dacutanan, 2020-Aug-16, Added code for write_file function in class FileProcessor
# Maria Dacutanan, 2020-Aug-16, Added del_inventory function in class DataProcessor
# Maria Dacutanan, 2020-Aug-18, Updated del_inventory function to delete duplicate entries
#------------------------------------------#

# -- DATA -- #
strChoice = '' # User input
lstTbl = []  # list of lists to hold data
dicRow = {}  # list of data row
strFileName = 'CDInventory.txt'  # data storage file
objFile = None  # file object
loadErr=False

# -- PROCESSING -- #
class DataProcessor:

    """Add or Delete Data from Inventory"""
    
    @staticmethod
    def add_newInventory(id, title, artist):
        """Function to add new data into CDInventory
        
        Args:
            id(string): id of new entry
            title(string): CD title of new entry
            artist(string): arist's name of new entry
        
        Returns:
            None
        """
        dicRow = {'ID': id, 'Title': title, 'Artist': artist}
        lstTbl.append(dicRow)
        return None
    
    @staticmethod
    def del_inventory(id):
        """Function to Delete from CDInventory
        
        Args:
            id(string)=id of entry in CDInventory that is to be deleted
        
        Returns:
            None
        """
        
        blnCDRemoved = False
        lstID=[]
        delctr=0
        for cd in lstTbl:                   
            for row in cd['ID']:
                lstID.append(row) #Store all IDs from lstTbl into lstID table
        if lstID.count(id) > 0: #Check if user input exists in lstID
            intRowNr = 0            
            #This while block will loop thru lstTbl to delete ALL instances of ID in case of duplicates
            while intRowNr < len(lstTbl):
                if (lstTbl[intRowNr]['ID']) == id:
                    del lstTbl[intRowNr]
                    delctr+=1 #Count number of deletions
                    intRowNr=0 #if ID was deleted, restart intRowNr as lstTbl has shifted
                else:
                    intRowNr += 1#increase intRowNr to move on to next index of lstTbl                         
            blnCDRemoved = True

        if blnCDRemoved:
            print('{} CD(s) removed.\n'.format(delctr))
        else:
            print('Could not find this CD!\n')
        return None


class FileProcessor:
    """Processing the data to and from text file"""

    @staticmethod
    def read_file(file_name, table):
        """Function to manage data ingestion from file to a list of dictionaries

        Reads the data from file identified by file_name into a 2D table
        (list of dicts) table one line in the file represents one dictionary row in table.

        Args:
            file_name (string): name of file used to read the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """
        table.clear()  # this clears existing data and allows to load data from file
        loadctr=0

        try:
            objFile=open(file_name, 'r') #open CDInventory.txt and store in objfile
            for line in objFile:
                data = line.strip().split(',')
                dicRow = {'ID': str(data[0]), 'Title': data[1], 'Artist': data[2]}
                table.append(dicRow)
                loadctr+=1 #count number of rows loaded into memory
            print ('{} CD(s) loaded into inventory.\n'.format(loadctr))
            return None
        except:
            print('Unable to load inventory from ' + file_name + '.\n') #if unable to load file, return error msg and break out of loop
            return None
        objFile.close()
    
    @staticmethod
    def write_file(file_name, table):
        """Function to Save CDInventory into File
        
        Args:
            file_name(file object)=filename of CDInventory file
            table(list)= list of CDInventory dictionaries
        
        Return:
            None
        """
        
        savectr=0
        objFile = open(file_name, 'w')
        for row in table:
            lstValues = list(row.values())
            objFile.write(','.join(lstValues) + '\n')
            savectr+=1 #counts number of rows saved into file
        objFile.close()        
        print ('{} CD(s) saved into {}.\n'.format(savectr,file_name))
        return None


# -- PRESENTATION (Input/Output) -- #

class IO:
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user

        Args:
            None.

        Returns:
            None.
        """

        print('Menu\n\n[l] load Inventory from file\n[a] Add CD\n[i] Display Current Inventory')
        print('[d] delete CD from Inventory\n[s] Save Inventory to file\n[x] exit\n')

    @staticmethod
    def menu_choice():
        """Gets user input for menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case sting of the users input out of the choices l, a, i, d, s or x

        """
        choice = ' '
        while choice not in ['l', 'a', 'i', 'd', 's', 'x']:
            choice = input('Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
        print()  # Add extra space for layout
        return choice

    @staticmethod
    def show_inventory(table):
        """Displays current inventory table


        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.

        """
        if (table):
            print('======= The Current Inventory: =======')
            print('ID\tCD Title (by: Artist)\n')
            for row in table:
                print('{}\t{} (by:{})'.format(*row.values()))
            print('======================================')
        else:
            print ('Inventory is empty.\n')
        return None

    @staticmethod
    def get_newInventory():
        while True: #user is re-prompted for null ID
            strID = str(input('Enter an ID: ').strip())
            if (strID):
                break
        while True: #user is re-prompted for null CD Title
            strTitle = input('Enter the CD\'s Title: ').strip()
            if (strTitle):
                break
        while True: #user is re-prompted for null Artist's Name
            strArtist = input('Enter the Artist\'s Name: ').strip()
            if (strArtist):
                break
        return (strID, strTitle, strArtist)

# 1. When program starts, read in the currently saved Inventory
FileProcessor.read_file(strFileName, lstTbl)

# 2. start main loop
while True:
    # 2.1 Display Menu to user and get choice
    IO.print_menu()
    strChoice = IO.menu_choice()

    # 3. Process menu selection
    # 3.1 process exit first
    if strChoice == 'x':
        break
    # 3.2 procless load inventory
    if strChoice == 'l':
            print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
            strYesNo = input('type \'yes\' to continue and reload from file. otherwise reload will be canceled: ')
            if strYesNo.lower() == 'yes':
                print('reloading...')
                FileProcessor.read_file(strFileName, lstTbl) # function call to read CDInventory.txt
                IO.show_inventory(lstTbl)
            else:
                input('canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')
                IO.show_inventory(lstTbl)
            continue  # start loop back at top.

    # 3.3 process add a CD
    elif strChoice == 'a':
        # 3.3.1 Ask user for new ID, CD Title and Artist
        intID,strTitle,strArtist=IO.get_newInventory() #function call to prompt user for ID, CD Title and Artist and unpack return values
        DataProcessor.add_newInventory(intID, strTitle, strArtist) #function call to add data into inventory
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.4 process display current inventory
    elif strChoice == 'i':
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.5 process delete a CD
    elif strChoice == 'd':
        # 3.5.1 get user input for which CD to delete
        # 3.5.1.1 display Inventory to user        
        if (lstTbl): #check if lstTbl is not empty
        # 3.5.1.2 ask user which ID to remove
            while True:
                intIDDel = input('Which ID would you like to delete? ').strip()
                if (intIDDel): #user is re-prompted for empty ID
                    DataProcessor.del_inventory(intIDDel) #function call to delete user provided ID
                    break
            IO.show_inventory(lstTbl)
        else:
            print('Nothing to delete. Inventory is empty.\n')
        continue  # start loop back at top.i
    # 3.6 process save inventory to file
    elif strChoice == 's':
        # 3.6.1 Display current inventory and ask user for confirmation to save
        if (lstTbl):
            IO.show_inventory(lstTbl)
            strYesNo = input('Save this inventory to file? [y/n] ').strip().lower()
            # 3.6.2 Process choice
            if strYesNo == 'y':
                # 3.6.2.1 save data
                FileProcessor.write_file(strFileName, lstTbl) #function call to write inventory into file
            else:
                input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')
        else:
            print('Nothing to save. Inventory is empty.\n')
        continue  # start loop back at top.
    # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be safe:
    else:
        print('General Error')




