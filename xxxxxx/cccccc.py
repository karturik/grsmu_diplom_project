def cities(input_string):
    output_string = input_string.split('\n')
    print(output_string)
    country1 = list(output_string[1].split(' '))
    print(country1)
    country2 = list(output_string[2].split(' '))
    print(country2)
    dict1 = {country1.pop(0):country1, country2.pop(0):country2}
    print(dict1.items())

input_string = "2\nRussia Moscow Petersburg Novgorod Kaluga\nUkraine Kiev Donetsk Odessa\n3\nOdessa\nMoscow\nNovgorod"

cities(input_string)