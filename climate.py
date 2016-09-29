
# -*- coding: utf-8 -*-

#-------------Modules----------------------------------------------------------
import sys
reload(sys)
sys.dont_write_bytecode = True
sys.setdefaultencoding('utf-8')

from csv import writer, QUOTE_ALL
from re import sub
from requests import get, post
from scrapy.selector import HtmlXPathSelector
from time import sleep

# Global variable initializaiton
items = []


#-------------Write header function--------------------------------------------
def csv_row_writer():
    # Builtin function to open file
    with open('climate.csv', 'w') as resource:
        writer(
            resource,
            delimiter=',',
            doublequote=True,
            lineterminator='\n',
            quoting=QUOTE_ALL,
            skipinitialspace=False,
        ).writerow([
            'Day',
            'T',
            'TM',
            'Tm',
            'SLP',
            'H',
            'PP',
            'VV',
            'V',
            'VM',
            'VG',
            'RA',
            'SN',
            'TS',
            'FG',
            'Location',
            'Year',
            'Month',
            'Weather Station',
            'Latitude',
            'Longitude',
            'Altitude'
        ])


# -------------Cleaning string function----------------------------------------
def get_cleaned_string(string):
    string = string.replace('\n', ' ')
    string = string.replace('\r', ' ')
    string = string.replace('\t', ' ')
    string = sub(r'[ ]+', ' ', string)
    string = string.strip()
    return string


def process():
    for page in range(1, 3):
        response_get = ''
        try:
            response_get = get(
                'http://en.tutiempo.net/climate/india/%(page)s/' % {
                    'page': page
                },
                timeout=10
            )
        except:
            pass
        hxs = ''
        try:
            hxs = HtmlXPathSelector(text=response_get.text)
        except:
            pass
        locations_url = ''
        try:
            locations_url = hxs.select(
                '//div[@class="DobleList"]/ul/li/a/@href'
            ).extract()
        except:
            pass
        for location_url in locations_url:
            print location_url
            for year in [
                2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015
            ]:
                response_get_month = ''
                try:
                    response_get_month = get(
                        'http://en.tutiempo.net/climate/%(year)s/'
                        '%(location_url)s' % {
                            'year': year,
                            'location_url': location_url.split('/')[-1]
                        },
                        timeout=10
                    )
                except:
                    pass
                hxs = ''
                try:
                    hxs = HtmlXPathSelector(text=response_get_month.text)
                except:
                    pass
                month_urls = ''
                try:
                    month_urls = hxs.select(
                        '//div[@class="SelClima"]/ul/li/a/@href'
                    ).extract()
                except:
                    pass
                for month_url in month_urls:
                    response_get_content = ''
                    try:
                        response_get_content = get(
                            'http://en.tutiempo.net%(month_url)s' % {
                                'month_url': month_url
                            },
                            timeout=10
                        )
                    except:
                        pass
                    print response_get_content
                    sleep(01)
                    hxs = ''
                    try:
                        hxs = HtmlXPathSelector(text=response_get_content.text)
                    except:
                        pass
                    try:
                        for td in hxs.select(
                            '//th[contains(text(), "Day")]/../'
                            'following-sibling::tr'
                        ):
                            day = ''
                            try:
                                day = td.select(
                                    './/td[1]/strong/text()'
                                ).extract()[0]
                            except:
                                pass
                            t = ''
                            try:
                                t = td.select('.//td[2]/text()').extract()[0]
                            except:
                                pass
                            tm = ''
                            try:
                                tm = td.select('.//td[3]/text()').extract()[0]
                            except:
                                pass
                            tm_ = ''
                            try:
                                tm_ = td.select('.//td[4]/text()').extract()[0]
                            except:
                                pass
                            slp = ''
                            try:
                                slp = td.select('.//td[5]/text()').extract()[0]
                            except:
                                pass
                            h = ''
                            try:
                                h = td.select('.//td[6]/text()').extract()[0]
                            except:
                                pass
                            pp = ''
                            try:
                                pp = td.select('.//td[7]/text()').extract()[0]
                            except:
                                pass
                            vv = ''
                            try:
                                vv = td.select('.//td[8]/text()').extract()[0]
                            except:
                                pass
                            v = ''
                            try:
                                v = td.select('.//td[9]/text()').extract()[0]
                            except:
                                pass
                            vm = ''
                            try:
                                vm = td.select('.//td[10]/text()').extract()[0]
                            except:
                                pass
                            vg = ''
                            try:
                                vg = td.select('.//td[11]/text()').extract()[0]
                            except:
                                pass
                            ra = ''
                            try:
                                ra = td.select('.//td[12]/text()').extract()[0]
                            except:
                                pass
                            sn = ''
                            try:
                                sn = td.select('.//td[13]/text()').extract()[0]
                            except:
                                pass
                            ts = ''
                            try:
                                ts = td.select('.//td[14]/text()').extract()[0]
                            except:
                                pass
                            fg = ''
                            try:
                                fg = td.select('.//td[15]/text()').extract()[0]
                            except:
                                pass
                            location = ''
                            try:
                                location = hxs.select(
                                    '//div[@class="titulo"]/h2/text()'
                                ).extract()[0]
                            except:
                                pass
                            month = ''
                            try:
                                month = hxs.select(
                                    '//div[@class="titulo"]/h2/span/text()'
                                ).extract()[0].split('-')[0]
                            except:
                                pass
                            weather_station = ''
                            try:
                                weather_station = hxs.select(
                                    '//p[1]/strong/text()'
                                ).extract()[0].split('-')[0]
                            except:
                                pass
                            latitude = ''
                            try:
                                latitude = hxs.select(
                                    '//p[1]/b[1]/text()'
                                ).extract()[0].split('-')[0]
                            except:
                                pass
                            longitude = ''
                            try:
                                longitude = hxs.select(
                                    '//p[1]/b[2]/text()'
                                ).extract()[0].split('-')[0]
                            except:
                                pass
                            altitude = ''
                            try:
                                altitude = hxs.select(
                                    '//p[1]/b[3]/text()'
                                ).extract()[0].split('-')[0]
                            except:
                                pass
                            items.append([
                                get_cleaned_string(day),
                                get_cleaned_string(t),
                                get_cleaned_string(tm),
                                get_cleaned_string(tm_),
                                get_cleaned_string(slp),
                                get_cleaned_string(h),
                                get_cleaned_string(pp),
                                get_cleaned_string(vv),
                                get_cleaned_string(v),
                                get_cleaned_string(vm),
                                get_cleaned_string(vg),
                                get_cleaned_string(ra),
                                get_cleaned_string(sn),
                                get_cleaned_string(ts),
                                get_cleaned_string(fg),
                                get_cleaned_string(location),
                                year,
                                get_cleaned_string(month),
                                get_cleaned_string(weather_station),
                                get_cleaned_string(latitude),
                                get_cleaned_string(longitude),
                                get_cleaned_string(altitude)
                            ])
                    except:
                        pass
    with open('climate.csv', 'a') as resource:
        writer(
            resource,
            delimiter=',',
            doublequote=True,
            lineterminator='\n',
            quoting=QUOTE_ALL,
            skipinitialspace=False,
        ).writerows(items)

csv_row_writer()
process()

