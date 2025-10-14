import os
import csv 

# load csv file as list of dict
def load_results(f):
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

        #if year key does not exist create
        if year not in species_yearly_avg:
            species_yearly_avg[year] = {}
        
         #if species key does not exist for that year create a list
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

    
data = load_results("penguins.csv")
avg = calc_yearly_avg_flipper_length(data)
print(avg)
over = calc_overall_yearly_average(avg)
print(over)
above = above_species_yearly_average(avg, over)
print (above)



