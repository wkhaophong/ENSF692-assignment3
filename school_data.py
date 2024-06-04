# school_data.py
# AUTHOR NAME: WARISA KHAOPHONG
#
# A terminal-based application for computing and printing statistics based on given input.
# You must include the main listed below. You may add your own additional classes, functions, variables, etc. 
# You may import any modules from the standard Python library.
# Remember to include docstrings and comments.

import numpy as np
from given_data import year_2013, year_2014, year_2015, year_2016, year_2017, year_2018, year_2019, year_2020, year_2021, year_2022

class SchoolData:
    """
    A class to handle the initialization and basic operations on school enrollment data.
    """
    def __init__(self):
        # List of yearly data
        self.years = [year_2013, year_2014, year_2015, year_2016, year_2017, year_2018, year_2019, year_2020, year_2021, year_2022]
        
        # Reshape each year data from 10x60 to 20x3 (row = school, col = grade)
        # Create a new 3D array with dimensions (years, schools, grades)
        self.enrollment_data = np.array([year.reshape(20, 3) for year in self.years])

        # Define a dictionary to map school codes to school names
        self.school_info = {
            1224: 'Centennial High School',
            1679: 'Robert Thirsk School',
            9626: 'Louise Dean School',
            9806: 'Queen Elizabeth High School',
            9813: 'Forest Lawn High School',
            9815: 'Crescent Heights High School',
            9816: 'Western Canada High School',
            9823: 'Central Memorial High School',
            9825: 'James Fowler High School',
            9826: 'Ernest Manning High School',
            9829: 'William Aberhart High School',
            9830: 'National Sport School',
            9836: 'Henry Wise Wood High School',
            9847: 'Bowness High School',
            9850: 'Lord Beaverbrook High School',
            9856: 'Jack James High School',
            9857: 'Sir Winston Churchill High School',
            9858: 'Dr. E. P. Scarlett High School',
            9860: 'John G Diefenbaker High School',
            9865: 'Lester B. Pearson High School'
        }
        self.school_codes = list(self.school_info.keys())
        self.school_names = list(self.school_info.values())

    def print_enrollment_data_array(self):
        """
        Print the shape and dimensions of the enrollment data array.
        """
        print("Shape of full data array:", self.enrollment_data.shape)
        print("Dimensions of full data array:", self.enrollment_data.ndim)

    def validate_input(self, school_code_or_name):
        """
        Validate the user input to ensure it is a valid school code or school name.
        
        Parameters:
        school_code_or_name (str): The input provided by the user, which can be either a school code or a school name.

        Returns:
        int: The validated school code corresponding to the provided input.
        """
        while True:
            try:
                # If input is a code, get the corresponding name
                if school_code_or_name.isdigit():
                    school_code_or_name = int(school_code_or_name)
                    if school_code_or_name not in self.school_codes:
                        raise ValueError("You must enter a valid school name or code.")
                    return school_code_or_name
                else:
                    # If the input is a name, find the corresponding code
                    match_found = False
                    for school_code, school_name in self.school_info.items():
                        if school_name.lower() == school_code_or_name.lower():  # Convert input to lowercase for case-insensitive comparison
                            match_found = True
                            return school_code

                    if not match_found:
                        raise ValueError("You must enter a valid school name or code.")
            except ValueError as ve:
                print(ve)
                school_code_or_name = input("Please enter a valid high school name or school code: ")

class SchoolStatistics:
    """
    A class to calculate and print statistics for a specific school.
    """
    def __init__(self, school_data):
        self.school_data = school_data

    def calculate_school_stats(self, school_code):
        """
        Calculate and print statistics for a specific school.
        
        Parameters:
        school_code (int): The code of the school for which statistics are to be calculated.
        """
        school_name = self.school_data.school_info[school_code]

        # Find index of the school in the array
        school_index = self.school_data.school_codes.index(school_code)

        # Extract school data from the array only 2 dimension years x grades
        school_data = self.school_data.enrollment_data[:, school_index, :]
        
        # Calculate statistics
        mean_enrollment_grade_10 = np.nanmean(school_data[:, 0])
        mean_enrollment_grade_11 = np.nanmean(school_data[:, 1])
        mean_enrollment_grade_12 = np.nanmean(school_data[:, 2])
        highest_enrollment = np.nanmax(school_data)
        lowest_enrollment = np.nanmin(school_data)
        total_enrollment_per_year = np.nansum(school_data, axis=1)
        total_ten_year_enrollment = np.nansum(total_enrollment_per_year)
        mean_total_yearly_enrollment = np.nanmean(total_enrollment_per_year)

        # Define a constant for the large class threshold
        LARGE_CLASS_THRESHOLD = 500
        # Masking operation to identify enrollments over large class threshold
        large_class_mask = school_data > LARGE_CLASS_THRESHOLD
        # Check if there are any enrollments over large class threshold
        if not np.any(large_class_mask):
            large_class_impact = "No enrollments over 500."
        else:
            # Calculate the median value of enrollments over 500
            large_class_impact = int(np.nanmedian(school_data[large_class_mask]))
        
        # Print the statistics
        print("\n***Requested School Statistics***\n")
        print(f"School Name: {school_name}, School Code: {school_code}")
        print(f"Mean enrollment for Grade 10: {int(mean_enrollment_grade_10)}")
        print(f"Mean enrollment for Grade 11: {int(mean_enrollment_grade_11)}")
        print(f"Mean enrollment for Grade 12: {int(mean_enrollment_grade_12)}")
        print(f"Highest enrollment for a single grade: {int(highest_enrollment)}")
        print(f"Lowest enrollment for a single grade: {int(lowest_enrollment)}")
            
        for year, enrollment in zip(range(2013, 2023), total_enrollment_per_year):
            print(f"Total enrollment for {year}: {int(enrollment)}")
                
        print(f"Total ten year enrollment: {int(total_ten_year_enrollment)}")
        print(f"Mean total enrollment over 10 years: {int(mean_total_yearly_enrollment)}")
        print(f"For all enrollments over 500, the median value was: {large_class_impact}")

class GeneralStatistics:
    """
    A class to calculate and print general statistics for all schools.
    """
    def __init__(self, school_data):
        self.school_data = school_data

    def print_general_stats(self):
        """
        Calculate and print general statistics for all schools over all years.
        """
        mean_enrollment_2013 = np.nanmean(self.school_data.enrollment_data[0])
        mean_enrollment_2022 = np.nanmean(self.school_data.enrollment_data[-1])
        total_graduating_class_2022 = np.nansum(self.school_data.enrollment_data[-1][:, 2])
        highest_enrollment_single_grade = np.nanmax(self.school_data.enrollment_data)
        lowest_enrollment_single_grade = np.nanmin(self.school_data.enrollment_data)
        
        print(f"Mean enrollment in 2013: {int(mean_enrollment_2013)}")
        print(f"Mean enrollment in 2022: {int(mean_enrollment_2022)}")
        print(f"Total graduating class of 2022: {int(total_graduating_class_2022)}")
        print(f"Highest enrollment for a single grade: {int(highest_enrollment_single_grade)}")
        print(f"Lowest enrollment for a single grade: {int(lowest_enrollment_single_grade)}")

def main():

    print("ENSF 692 School Enrollment Statistics\n")
    
    # Create an instance of SchoolData
    school_data = SchoolData()

    # Print the shape and dimensions of the array for Stage 1 requirements 
    school_data.print_enrollment_data_array()

    # Prompt for user input
    user_input = input("\nPlease enter the high school name or school code: ")
   
    # Validate user input
    validated_input = school_data.validate_input(user_input)
    if validated_input is not None:
        # Calculate school statistics and Print Stage 2 requirements
        school_stats = SchoolStatistics(school_data)
        school_stats.calculate_school_stats(validated_input)

    # Calculate general statistics and Print Stage 3 requirements 
    print("\n***General Statistics for All Schools***\n")
    general_stats = GeneralStatistics(school_data)
    general_stats.print_general_stats()

if __name__ == '__main__':
    main()
