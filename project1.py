# SI 201 HW4
# Your name: Jessica Moon
# Your student id: 44434120
# Your email: djmoon@umich.edu
# Who or what you worked with on this homework (including generative AI like ChatGPT): I asked Chatgpt hints for debugging and suggesting the general sturcture of the code

import os
import csv 

# load csv file as list of dict
def read_penguin_data(f):
    base_path = os.path.abspath(os.path.dirname(__file__))
    full_path = os.path.join(base_path, f)

    with open(full_path, newline = '') as fh:
        r = csv.DictReader(fh)
        data = list(r)
    return data

#calculate avg flipper length per species for each year
def calc_yearly_avg_flipper_length(data):
    species_yearly_avg = {} #nested dict {year: {species: [flipper_lengths]}}

    for row in data:
        species = row.get("species")
        year = row.get("year")
        flipper = row.get("flipper_length_mm")

        #skip rows that has missing data
        if not (species and year and flipper):
            continue

        #skips rows where flipper length is NA
        if flipper == "NA":
            continue

        flipper = float(flipper)

        #if year key does not exist in the dict create new inner dict
        if year not in species_yearly_avg:
            species_yearly_avg[year] = {}
        
         #if species key does not exist for that year create a empty list
        if species not in species_yearly_avg[year]:
            species_yearly_avg[year][species] = []

        # add flipper length value to the corresponding list
        species_yearly_avg[year][species].append(flipper)
    
    # calculate avg flipper length for each species each year
    for year in species_yearly_avg:
        for species in species_yearly_avg[year]:
            lengths = species_yearly_avg[year][species]
            avg = sum(lengths) / len(lengths)
            species_yearly_avg[year][species] = avg #replace list with avg value
    
    return species_yearly_avg

#calculate the overall yearly average(across all the species per year)
def calc_overall_yearly_average(species_yearly_avg):
    overall_yearly_avg = {}

    # loop through each year and its species data
    for year, species_data in species_yearly_avg.items():
        avg_values = list(species_data.values()) #extract all species average for that year

        #skip years that have no data
        if len(avg_values) == 0:
            continue

        #calculate mean of species avg for that year
        overall_avg = sum(avg_values) / len(avg_values)
        overall_yearly_avg[year] = overall_avg

    return overall_yearly_avg

#identify species whose yearly avg flipper length is above the yearly mean
def above_species_yearly_average(species_yearly_avg, overall_yearly_avg):
    above_avg_penguins = {}

    #loop through each year and compare species avg to the overall avg
    for year, species_data in species_yearly_avg.items():
        year_avg = overall_yearly_avg.get(year)
        if not year_avg: #skip if year not found
            continue 
        
        above_avg_penguins[year] = [] 

        # compare each species avg to the overall mean for that year
        for species,avg in species_data.items():
            #if species abg flipper lenght is above the mean add to the list
            if avg > year_avg:
                above_avg_penguins[year].append(species)
    return above_avg_penguins

def write_results(species_yearly_avg, overall_yearly_avg, above_avg_penguins, filename = "penguin_report.csv"):
    with open(filename, 'w', newline="") as f:
        write = csv.writer(f)

        write.writerow(["Year", "Species", "Species_Avg_flipper_lengths(mm)", "Overall_Avg_flipper_lengths(mm)", "Status"])
    
        for year in species_yearly_avg:
            for species, avg in species_yearly_avg[year].items():

                if species in above_avg_penguins.get(year,[]):
                    status = "Above Average"
                else:
                    status = "Below Average"

                write.writerow([
                    year,
                    species,
                    avg,
                    overall_yearly_avg[year],
                    status
                ])

import unittest

class PenguinTest(unittest.TestCase):
    def setUp(self):
        self.penguin_dict = [
            {"species": "Adelie", "year": "2007", "flipper_length_mm": "197"},
            {"species": "Adelie", "year": "2008", "flipper_length_mm": "220"},
            {"species": "Gentoo", "year": "2008", "flipper_length_mm": "200"},
            {"species": "Chinstrap", "year": "2009", "flipper_length_mm": "NA"},
            {"species": "Chinstrap", "year": "2009", "flipper_length_mm": "195"}
            ]
        self.species_avg = calc_yearly_avg_flipper_length(self.penguin_dict)
        self.overall_avg = calc_overall_yearly_average(self.species_avg)
        self.above_avg = above_species_yearly_average(self.species_avg, self.overall_avg)

#-----------------------------------
# calc_yearly_avg_flipper_length TEST
#-----------------------------------

    def test_calc_yearly_avg_flipper_length(self):
        #test case 1
        self.assertAlmostEqual(self.species_avg["2009"]["Chinstrap"], 195.0)
        #test case 2
        self.assertTrue("Adelie" in self.species_avg["2008"].keys(), True)

        #edge cases 1
    def test_yearly_empty_data(self):
        result = calc_yearly_avg_flipper_length([])
        self.assertEqual(result, {})

        #edge cases 2
    def test_yearly_avg_all_na(self):
        only_na = [
            {"species": "Adelie", "year": "2007", "flipper_length_mm": "NA"},
            {"species": "Adelie", "year": "2008", "flipper_length_mm": "NA"}
        ]
        result = calc_yearly_avg_flipper_length(only_na)
        self.assertEqual(result, {})

#-----------------------------------
# calc_overall_yearly_average TEST
#-----------------------------------

    def test_calc_overall_yearly_average(self):
        #test case 1
        expected_avg = (200+220)/2
        self.assertAlmostEqual(self.overall_avg["2008"], expected_avg)
        #test case 2
        self.assertIn("2007", self.overall_avg)
       
        #edge cases 1
    def test_overall_avg_edge_empty_dict(self):
        result = calc_overall_yearly_average({})
        self.assertEqual(result, {})
        #edge cases 2
    def test_overall_avg_edge_no_species(self):
        result = calc_overall_yearly_average({"2009": {}})
        self.assertEqual(result,{})

#-----------------------------------
# above_species_yearly_average TEST
#-----------------------------------
    
    def test_above_species_yearly_average(self):
        #test case 1
        self.assertEqual(self.above_avg["2008"], ["Adelie"])
        #test case 2
        self.assertEqual(self.above_avg["2009"], [])
        
        #edge cases 1
    def test_above_avg_empty_inputs(self):
        result = above_species_yearly_average({}, {})
        self.assertEqual(result, {})

        #edge cases 2
    def test_above_missing_year(self):
        fake_overall = {"2010": 210}
        result = above_species_yearly_average(self.species_avg, fake_overall)
        self.assertEqual(result, {})

     
if __name__ == '__main__':
    
     data = read_penguin_data("penguins.csv")
     
     species_yearly_avg = calc_yearly_avg_flipper_length(data)
     overall_yearly_avg = calc_overall_yearly_average(species_yearly_avg)
     above_avg_penguins = above_species_yearly_average(species_yearly_avg, overall_yearly_avg)
     write_results(species_yearly_avg,overall_yearly_avg,above_avg_penguins)

     unittest.main(verbosity=2)




