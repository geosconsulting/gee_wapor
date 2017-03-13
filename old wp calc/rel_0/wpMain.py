import argparse
import datetime
# import sys

from wpCalc import L1WaterProductivity


def valid_date(s):
    try:
        return datetime.datetime.strptime(s, "%Y-%m-%d").date()
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)


def main(args=None):

    parser = argparse.ArgumentParser(
        description='Water Productivity using Google Earth Engine')
    groupTimePeriod = parser.add_mutually_exclusive_group()
    groupTimePeriod.add_argument("-a",
                                 "--annual",
                                 metavar='Year',
                                 type=int,
                                 help="Calculate Water Productivity Annually"
                                      " - Year must be provided",
                                 default=0)

    groupTimePeriod.add_argument("-d",
                                 "--dekadal",
                                 metavar="Start Date YYYY-MM-DD, "
                                         "End Date YYYY-MM-DD",
                                 help="Calculate Water Productivity for ten"
                                      " days - Starting and ending date must"
                                      " be provided with the following "
                                      "format YYYY-MM-DD",
                                 nargs=2,
                                 type=valid_date)

    parser.add_argument("-v", "--verbose",
                        help="Increase output verbosity",
                        action="store_true")

    group_output = parser.add_mutually_exclusive_group()
    group_output.add_argument("-c",
                              "--chart",
                              help="Each calculated component (AGBP, AET, WPm)"
                                   " shown on a chart",
                              action="store_true")
    group_output.add_argument("-m",
                              "--map",
                              help="Show the final output overlaid "
                                   " on Google Map",
                              action="store_true")

    parser.add_argument('-e', '--export', choices=['u', 'd', 'a', 'g', 'n'],
                        help="Choose export to url(-u), drive (-d), "
                             " asset (-t) or geoserver (-g)")

    parser.add_argument('-s', '--switch', type=float,
                        help="Replace the Above Ground Biomass Production with Net Primary Productivity multiplied "
                             "by a constant value. Sending -s 1.25 will set agbp=npp * 1.25. If not provided default "
                             "datasets will be used instead")

    results = parser.parse_args()
    print(results)

    elaborazione = L1WaterProductivity()

    if results.switch:
        moltiplicatore = results.switch
        elaborazione.multi_agbp = moltiplicatore
        abpmmmm = elaborazione.multi_agbp

    if results.annual:
        if results.chart:
            abpm, aet = elaborazione.image_selection_annual()

            L1_AGBP_summed, ETaColl1, ETaColl2, ETaColl3, WPbm = elaborazione.image_processing(abpm, aet)

            elaborazione.image_visualization('c',
                                             L1_AGBP_summed,
                                             ETaColl3,
                                             WPbm)
        elif results.map:
            abpm, aet = elaborazione.image_selection_annual()
            L1_AGBP_summed, ETaColl1, ETaColl2, ETaColl3, WPbm = elaborazione.image_processing(abpm, aet)
            elaborazione.image_visualization('m',
                                             L1_AGBP_summed,
                                             ETaColl3,
                                             WPbm)
        else:
            abpm, aet = elaborazione.image_selection_annual()
            L1_AGBP_summed, ETaColl1, ETaColl2, ETaColl3, WPbm = elaborazione.image_processing(abpm, aet)

    else:
        abpm, aet = elaborazione.image_selection(results.dekadal[0],
                                                 results.dekadal[1])
        L1_AGBP_summed, ETaColl1, ETaColl2, ETaColl3, WPbm = elaborazione.image_processing(abpm, aet)
        if results.chart:
            elaborazione.image_visualization('c',
                                             L1_AGBP_summed,
                                             ETaColl3,
                                             WPbm)
        elif results.map:
            elaborazione.image_visualization('m',
                                             L1_AGBP_summed,
                                             ETaColl3,
                                             WPbm)

    elaborazione.image_export(results.export, WPbm)

if __name__ == '__main__':
    main()
