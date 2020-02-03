'''Version 0.35'''

from time import perf_counter

from src import awards, hosts, nominees, presenters, winners
from util.load import load_json, dump_json

OFFICIAL_AWARDS_1315 = [
    'cecil b. demille award',
    'best motion picture - drama',
    'best performance by an actress in a motion picture - drama',
     'best performance by an actor in a motion picture - drama',
     'best motion picture - comedy or musical',
     'best performance by an actress in a motion picture - comedy or musical',
     'best performance by an actor in a motion picture - comedy or musical',
     'best animated feature film',
     'best foreign language film',
     'best performance by an actress in a supporting role in a motion picture',
     'best performance by an actor in a supporting role in a motion picture',
     'best director - motion picture',
     'best screenplay - motion picture',
     'best original score - motion picture',
     'best original song - motion picture',
     'best television series - drama',
     'best performance by an actress in a television series - drama',
     'best performance by an actor in a television series - drama',
     'best television series - comedy or musical',
     'best performance by an actress in a television series - comedy or musical',
     'best performance by an actor in a television series - comedy or musical',
     'best mini-series or motion picture made for television',
     'best performance by an actress in a mini-series or motion picture made for television',
     'best performance by an actor in a mini-series or motion picture made for television',
     'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television',
     'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television'
     ]

OFFICIAL_AWARDS_1819 = [
    'best motion picture - drama',
    'best motion picture - musical or comedy',
    'best performance by an actress in a motion picture - drama',
    'best performance by an actor in a motion picture - drama',
    'best performance by an actress in a motion picture - musical or comedy',
    'best performance by an actor in a motion picture - musical or comedy',
    'best performance by an actress in a supporting role in any motion picture',
    'best performance by an actor in a supporting role in any motion picture',
    'best director - motion picture', 'best screenplay - motion picture',
    'best motion picture - animated', 'best motion picture - foreign language',
    'best original score - motion picture', 'best original song - motion picture',
    'best television series - drama', 'best television series - musical or comedy',
    'best television limited series or motion picture made for television',
    'best performance by an actress in a limited series or a motion picture made for television',
    'best performance by an actor in a limited series or a motion picture made for television',
    'best performance by an actress in a television series - drama',
    'best performance by an actor in a television series - drama',
    'best performance by an actress in a television series - musical or comedy',
    'best performance by an actor in a television series - musical or comedy',
    'best performance by an actress in a supporting role in a series, limited series or motion picture made for television',
    'best performance by an actor in a supporting role in a series, limited series or motion picture made for television',
    'cecil b. demille award'
    ]


def get_hosts(year):
    '''Hosts is a list of one or more strings. Do NOT change the name
    of this function or what it returns.'''
    # Your code here
    hosts = load_json('results/', year)['hosts']
    return hosts

def get_awards(year):
    '''Awards is a list of strings. Do NOT change the name
    of this function or what it returns.'''
    awards = load_json('results/', year)['award_names']
    return awards

def get_nominees(year):
    '''Nominees is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change
    the name of this function or what it returns.'''
    # Your code here
    award_map = load_json('results/', year)['award_data']
    awards = award_map.keys()
    nominees = {award : award_map[award]['nominees'] for award in awards}
    return nominees

def get_winner(year):
    '''Winners is a dictionary with the hard coded award
    names as keys, and each entry containing a single string.
    Do NOT change the name of this function or what it returns.'''
    # Your code here
    award_map = load_json('results/', year)['award_data']
    awards = award_map.keys()
    winners = {award : award_map[award]['winner'] for award in awards}
    return winners

def get_presenters(year):
    '''Presenters is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change the
    name of this function or what it returns.'''
    # Your code here
    award_map = load_json('results/', year)['award_data']
    awards = award_map.keys()
    presenters = {award : award_map[award]['presenters'] for award in awards}
    return presenters

def pre_ceremony():
    '''This function loads/fetches/processes any data your program
    will use, and stores that data in your DB or in a json, csv, or
    plain text file. It is the first thing the TA will run when grading.
    Do NOT change the name of this function or what it returns.'''
    # Your code here

    print("Pre-ceremony processing complete.")
    return

def main():
    '''This function calls your program. Typing "python gg_api.py"
    will run this function. Or, in the interpreter, import gg_api
    and then run gg_api.main(). This is the second thing the TA will
    run when grading. Do NOT change the name of this function or
    what it returns.'''
    # Your code here

    years = ['2013']

    for year in years:
        data = load_json('data/', year)
        to_dump = {}

        # EXTRACT & TIME
        t0 = perf_counter()
        host_names = hosts.extract(data)
        t1 = perf_counter()
        to_dump['hosts'] = host_names
        award_names = awards.extract(data)
        t2 = perf_counter()
        to_dump['award_names'] = award_names
        nomi_map = nominees.extract(data)
        t3 = perf_counter()
        pres_map = presenters.extract(data)
        t4 = perf_counter()
        winn_map = winners.extract(data)
        tf = perf_counter()

        # DISPLAY TIMES
        print("Host names extracted in : ", round(t1 - t0, 2), " seconds.")
        print("Award names extracted in : ", round(t2 - t1, 2), " seconds.")
        print("Nominees extracted in : ", round(t3 - t2, 2), " seconds.")
        print("Presenters extracted in : ", round(t4 - t3, 2), " seconds.")
        print("Winners extracted in : ", round(tf - t4, 2), " seconds.")
        print("Cumulative time to perform all tasks : ", round(tf - t0, 2), " seconds.")

        award_map = {}

        true_award_list = OFFICIAL_AWARDS_1315
        if year == '2018' or year == '2019':
            true_award_list = OFFICIAL_AWARDS_1819

        for award in true_award_list:
                award_map[award] = {}
                noms = []
                pres = []
                winn = ''

                try:
                    noms = nomi_map[award]
                except KeyError:
                    pass

                try:
                    pres = pres_map[award]
                except KeyError:
                    pass

                try:
                    winn = winn_map[award]
                except KeyError:
                    pass

                award_map[award]['nominees'] = noms
                award_map[award]['presenters'] = pres
                award_map[award]['winner'] = winn

        to_dump['award_data'] = award_map

        # for testing
        dump_json('results/', year, to_dump)

    print("Done.")
    return

if __name__ == '__main__':
    main()
